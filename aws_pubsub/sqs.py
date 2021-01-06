"""SQS Baqckend for PubSub"""

import json
import logging

import boto3
from django.conf import settings
from django.utils.functional import LazyObject, cached_property

logger = logging.getLogger("default")


class Sqs(object):
    """SQS Management class."""

    def __init__(self):
        self.topic_name = settings.WORKER_CONFIG["TOPIC_NAME"]
        self.user_mode = settings.WORKER_CONFIG.get("USER_MODE", False)
        self.region = settings.WORKER_CONFIG.get("REGION", "us-east-1")
        self._queue_name = settings.WORKER_CONFIG["QUEUE_NAME"]
        self._deadletter_queue_name = settings.WORKER_CONFIG.get(
            "DEADLETTER_QUEUE_NAME", None
        )
        self.sqs_client = boto3.client("sqs", region_name=self.region)

        self.set_sns_topic(self.topic_name, region=self.region)
        self.set_sqs_queue(self.queue_name, self.topic)

    def ack_messages(self, receipts, max_retries=10):
        entries = [{"Id": str(k), "ReceiptHandle": v} for k, v in enumerate(receipts)]

        if not any(entries):
            return

        response = self.sqs_client.delete_message_batch(
            QueueUrl=self.queue, Entries=entries
        )

        failed = response.get("Failed", [])

        while len(failed) and max_retries > 0:
            retry = [{"Id": x["Id"], "ReceiptHandle": entries[x["Id"]]} for x in failed]
            response = self.sqs_client.delete_message_batch(
                QueueUrl=self.queue, Entries=retry
            )
            max_retries -= 1

    def destroy_app_sqs_queue(self, sns_arn, queue_url, nextToken):
        pass
        # TODO: Build this out

    def send_task(self, messages, task_name, delay=None):
        entries = []
        for _id, message in enumerate(messages):
            message["Type"] = task_name

            msg = {"Id": "{}".format(_id), "MessageBody": json.dumps(message)}

            if delay:
                msg["DelaySeconds"] = delay

            entries.append(msg)

        response = self.sqs_client.send_message_batch(
            QueueUrl=self.queue, Entries=entries
        )
        logger.info(json.dumps(response))

    def enqueue(self, messages, task, delay=None):
        """Enqeue messages to sqs.

        Args:
        messages (list(dict): Messages to qneue
        task (function): task function
        delay (:obj: int, optional): Delay in seconds
        """
        self.send_task(messages, "%s.%s" % (task.__module__, task.__name__), delay)

    @cached_property
    def username(self):
        """Gets iam Username if in user mode

        Returns:
            (str): IAM username
        """
        if self.user_mode:
            iam = boto3.client("iam")
            user = iam.get_user()
            return user["User"]["UserName"]

    @property
    def queue_name(self):
        """Gets iam Username if in user mode

        Returns:
            str: IAM username
        """
        if self.user_mode:
            return "-".join([self._queue_name, self.username])
        else:
            return self._queue_name

    def get_queue_deadletter(self):
        if self._deadletter_queue_name:
            return self._deadletter_queue_name
        return self.queue_name + "-deadletter"

    def get_user_mode_queue_key(self, key):
        return key + "-" + self.get_iam_username()

    def recieve(self):
        response = self.sqs_client.receive_message(
            QueueUrl=self.queue, MaxNumberOfMessages=10, WaitTimeSeconds=20
        )
        return response.get("Messages", None)

    def set_sns_topic(self, topic_name, region="us-east-1"):
        sns = boto3.client("sns", region_name=region)
        response = sns.create_topic(Name=topic_name)

        self.topic = response["TopicArn"]

    def set_sqs_queue(
        self, queue_name, sns_arn, max_receive_count=5, region="us-east-1"
    ):
        sqs = boto3.client("sqs", region_name=region)
        sns = boto3.client("sns", region_name=region)

        dead_name = self.get_queue_deadletter()
        queue = sqs.create_queue(QueueName=queue_name)
        deadletter = sqs.create_queue(QueueName=dead_name)
        dead_attrs = sqs.get_queue_attributes(
            QueueUrl=deadletter["QueueUrl"], AttributeNames=["QueueArn"]
        )

        queue_attrs = sqs.get_queue_attributes(
            QueueUrl=queue["QueueUrl"], AttributeNames=["QueueArn"]
        )
        queue_arn = queue_attrs["Attributes"]["QueueArn"]
        dead_letter_queue_arn = dead_attrs["Attributes"]["QueueArn"]

        redrive_policy = {
            "deadLetterTargetArn": dead_letter_queue_arn,
            "maxReceiveCount": "{}".format(max_receive_count),
        }

        policy = {
            "Version": "2012-10-17",
            "Id": "{0}/SQSDefaultPolicy".format(queue_arn),
            "Statement": [
                {
                    "Sid": "rule1",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "SQS:*",
                    "Resource": queue_arn,
                    "Condition": {"StringEquals": {"aws:SourceArn": sns_arn}},
                }
            ],
        }
        sqs.set_queue_attributes(
            QueueUrl=queue["QueueUrl"],
            Attributes={
                "RedrivePolicy": json.dumps(redrive_policy),
                "Policy": json.dumps(policy),
            },
        )

        filter_policy = {"routing-key": [queue_name]}

        sns.subscribe(
            TopicArn=sns_arn,
            Protocol="sqs",
            Endpoint=queue_arn,
            Attributes={"FilterPolicy": json.dumps(filter_policy)},
        )

        self.queue = queue["QueueUrl"]


class SqsBackend(LazyObject):
    def _setup(self):
        self._wrapped = Sqs()


backend = SqsBackend()


def enqueue(messages, task, delay=None):
    backend.enqueue(messages, task, delay)


def send_task(messages, task_name, delay=None):
    backend.send_task(messages, task_name, delay)


def ack_messages(receipts):
    backend.ack_messages(receipts)


def queue_name():
    return backend.queue_name


def get_messages():
    return backend.recieve()
