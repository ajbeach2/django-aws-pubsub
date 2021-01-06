import uuid
import json
from django.test import TestCase
from aws_pubsub.dispatcher import process


class TestTasks(TestCase):
    def test_notificaiton_message(self):
        message = {
            "MessageId": str(uuid.uuid4()),
            "ReceiptHandle": 12345,
            "Body": json.dumps({
                "Type": "Notification",
                "MessageId": str(uuid.uuid4()),
                "TopicArn": "arn:aws:sns:us-east-1:111111111111:my-topic",
                "Message": '{\"Message\":{\"Task\":\"cat\"}}',
            }),
        }

        receipt_handle, result = process(message)
        self.assertEqual(receipt_handle, 12345)
        self.assertEqual(result, "meow")
