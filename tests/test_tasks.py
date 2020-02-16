from django.test import TestCase
from aws_pubsub import task_manager, exceptions


class TestTasks(TestCase):
    def test_setup(self):
        self.assertIsNot(task_manager.manager._registry, {})

    def test_default_register(self):
        self.assertTrue(
            task_manager.get_task("tests.tasks.duck")
        )
        try:
            task_manager.get_task("tests.tasks.duck")
        except exceptions.TaskNotFound:
            self.fail("Task tests.tasks.duck should exist!")
