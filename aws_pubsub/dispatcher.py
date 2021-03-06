"""PubSub Consumer."""
from datetime import datetime
import json
import logging
from time import process_time
import traceback
from typing import Any, Tuple, List

from .task_manager import get_task

logger = logging.getLogger("default")


def _get_task_name(obj):
    return obj.get("Type", obj.get("Task", None))


def _get_task_input(msg: dict, msg_type: str) -> dict:
    if msg_type == "Notification":
        return json.loads(msg.get("Message", None))
    return msg


def process_task(body: dict) -> Tuple[str, int]:
    """ TODO: refactor to not repeat code."""
    task_name = _get_task_name(body)
    func = get_task(task_name)
    start = process_time()
    result = func(body)
    end = process_time()

    return (
        result,
        (end - start) * 1000,
    )


def process(message: dict) -> Tuple[str, Any]:
    """Process a task message.

    Args:
        message (dict): Incomming message from SQS
    Returns:
        (str, :obj): recipte handle and result
    """
    body = json.loads(message["Body"])
    source = body.get("Type", None)

    # if source is sns do extra message key
    if source == "Notification":
        body = json.loads(body.get("Message", None))

    task_input = body.get("Message", {})
    task_name = task_input.get("Task", None)

    func = get_task(task_name)

    logger.debug(
        {
            "message_id": message["MessageId"],
            "event": "worker.processing",
            "task": task_name,
            "message": message,
            "timestamp": datetime.utcnow().__str__(),
        }
    )

    start = process_time()
    result = func(task_input)
    end = process_time()

    logger.debug(
        {
            "message_id": message["MessageId"],
            "event": "worker.success",
            "message": message,
            "result": result,
            "timestamp": datetime.utcnow().__str__(),
            "duration": (end - start) * 1000,
        }
    )
    receipt_handle = message.get("ReceiptHandle", None)

    return receipt_handle, result


def dispatch(messages: List[dict]):
    """Dispatches messages to tasks that are registered.

    Args:
        messages (dict): Messages recieved from sqs
    Returns:
        list(string): Reciept handles if they exist
    """
    receipt_handles = []

    for message in messages:
        try:
            receipt_handle, result = process(message)
        except (KeyboardInterrupt, SystemExit) as e:
            raise e
        except Exception as exception:  # pylint: disable=W0703
            logger.error(
                {
                    "message_id": message["MessageId"],
                    "event": "worker.error",
                    "error": exception.__str__(),
                    "stacktrace": traceback.format_exc(),
                    "message": message,
                    "timestamp": datetime.utcnow().__str__(),
                }
            )
            continue

        if receipt_handle:
            receipt_handles.append(receipt_handle)

    return receipt_handles
