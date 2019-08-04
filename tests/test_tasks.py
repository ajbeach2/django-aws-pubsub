from django.test import TestCase
from aws_pubsub import task_manager


class TestTasks(TestCase):
    def test_setup(self):
        self.assertIsNot(task_manager.manager._registry, {})
