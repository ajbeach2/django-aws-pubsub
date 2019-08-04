"""Django App config"""

from django.apps import AppConfig
from django.core import checks

from .checks import check_settings


class AwsPubsubConfig(AppConfig):
    """AwsPubsub config class."""

    name = "aws_pubsub"

    def ready(self):
        checks.register(check_settings, "worker")
        self.module.autodiscover()
