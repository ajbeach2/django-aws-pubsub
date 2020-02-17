from importlib import import_module

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.utils.functional import LazyObject


__all__ = ["enqueue", "send_task", "get_messages", "ack_messages"]


def load_backend(backend_name):
    """
    Return a aws_pubsub backend's "base" module given a fully qualified
    backend name, or raise an error if it doesn't exist.
    """
    try:
        return import_module("%s" % backend_name)
    except ImportError as e_user:
        raise ImproperlyConfigured(
            "%r isn't an available aws_pubsub backend.\n"
            "Try using 'aws_pubsub.backends.XXX', where XXX is one of:\n"
            "    %s" % (backend_name, ", ".join(["sqs", "sql"]))
        ) from e_user


backend_cls = load_backend(
    settings.WORKER_CONFIG.get("BACKEND", "aws_pubsub.backends.sql")
)


class Backend(LazyObject):
    def _setup(self):
        self._wrapped = backend_cls.BackendWrapper()


backend = Backend()


def enqueue(messages, task, delay=None):
    """Send a task to the qeue.

    Args:
        messages (list(dict)): Task function
        task (function): Task function to queue
        delay (number): Delay to send message
    """
    backend.enqueue(messages, task, delay)


def send_task(messages, task_name, delay=None):
    """Send a task to the qeue.

    Args:
        messages (list(dict)): List of messages to send to the queue
        task_name (str): Import path string of task
        delay (number): Delay to send message
    """
    backend.send_task(messages, task_name, delay)


def ack_messages(receipts):
    backend.ack_messages(receipts)


def get_messages():
    return backend.recieve()
