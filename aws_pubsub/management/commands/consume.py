import multiprocessing

from django.core.management.base import BaseCommand

from aws_pubsub.consumers import Consumer


class Command(BaseCommand):
    help = "start consumer(s) of tasks"

    # http://jtushman.github.io/blog/2014/01/14/python-%7C-multiprocessing-and-interrupts/
    def handle(self, *args, **options):
        # Restart processes when max tasks is reached
        # python hack to free memory on long running processes
        Consumer().run()
