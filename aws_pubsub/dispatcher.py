"""PubSub Consumer."""
from datetime import datetime
import json
import logging
from time import process_time
import traceback
from typing import Any, Tuple, List

from .task_manager import get_task

logger = logging.getLogger("default")


def _get_task_input(msg: dict, msg_type: str) -> dict:
    if msg_type == "Notification":
        return json.loads(msg.get("Message", None))
    return msg


def process(message: dict) -> Tuple[str, Any]:
    """Process a task message.

    Args:
        message (dict): Incomming message from SQS
    Returns:
        (str, :obj): recipte handle and result
    """
    msg = json.loads(message["Body"])
    msg_type = msg.get("Type", None)

    task_input = _get_task_input(msg, msg_type)
    task_name = task_input.get("Type", None)

    func = get_task(task_name)

    logger.info(
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

    logger.info(
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
