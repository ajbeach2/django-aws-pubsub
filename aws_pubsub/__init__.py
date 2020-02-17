"""AwsPubSub Module for Django."""

from django.utils.module_loading import autodiscover_modules

from aws_pubsub.backends import enqueue, send_task
from aws_pubsub.task_manager import manager, register

__all__ = ["enqueue", "register", "send_task"]


def autodiscover():
    """registers tasks through module discovery."""
    autodiscover_modules("tasks", register_to=manager)


default_app_config = "aws_pubsub.apps.AwsPubsubConfig"
