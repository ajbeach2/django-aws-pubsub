"""Run a taskfrom command line."""

import json

from django.core.management.base import BaseCommand

from aws_pubsub import send_task


class Command(BaseCommand):
    help = "Run a taskfrom command line"

    def add_arguments(self, parser):
        parser.add_argument(
            "task", nargs=1, help="Task Name",
        )

        parser.add_argument(
            "payload", nargs="+", help="Task Payload(s)",
        )

    def handle(self, *args, **options):
        for task in options["task"]:
            messages = [json.loads(payload) for payload in options["payload"]]
            send_task(messages, task)
