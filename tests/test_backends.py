from django.test import TestCase
from aws_pubsub import enqueue
from .tasks import duck
from aws_pubsub.consumers import Consumer


class TestBackends(TestCase):

    def test_queue_tasks(self):
        enqueue([{}], duck)
        self.assertTrue(Consumer().run())
