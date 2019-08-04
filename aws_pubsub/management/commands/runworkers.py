import multiprocessing

from django.core.management.base import BaseCommand

from aws_pubsub.consumers import MultiProcessConsumer


class Command(BaseCommand):
    help = "start consumer(s) of tasks"

    def add_arguments(self, parser):
        parser.add_argument(
            "--workers",
            default=multiprocessing.cpu_count() * 2,
            help="Run workers in debug mode",
        )

        parser.add_argument(
            "--max_tasks_per_child",
            default=10000,
            help="Number of gets before workers processes are respawned",
        )

    # http://jtushman.github.io/blog/2014/01/14/python-%7C-multiprocessing-and-interrupts/
    def handle(self, *args, **options):
        self.workers = options.get("workers")
        self.max_tasks_per_child = options.get("max_tasks_per_child")
        print("Creating {} consumers".format(self.workers))

        # Restart processes when max tasks is reached
        # python hack to free memory on long running processes
        while True:
            consumers = [
                MultiProcessConsumer(i, self.max_tasks_per_child)
                for i in range(self.workers,)
            ]
            for w in consumers:
                w.start()

            try:
                for w in consumers:
                    w.join()
            except (KeyboardInterrupt, SystemExit):
                break
