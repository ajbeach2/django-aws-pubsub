"""System Checks for aws_pubsub"""

from django.conf import settings
from django.core.checks import Error


def check_settings(app_configs, **kwargs):
    """Check Configuration Settings."""
    if not hasattr(settings, "WORKER_CONFIG"):
        return [
            Error(
                "You must configure WORKER_CONFIG in your settings",
                id="aws_pubsub.E001",
            )
        ]

    errors = []

    requires = {"QUEUE_NAME": "aws_pubsub.E002", "TOPIC_NAME": "aws_pubsub.E003"}

    for key, err in requires.items():
        if key not in settings.WORKER_CONFIG:
            errors.append(
                Error(
                    'WORKER_CONFIG must contain "{}"'.format(key),
                    obj="WORKER_CONFIG",
                    id=err,
                )
            )

    return errors
