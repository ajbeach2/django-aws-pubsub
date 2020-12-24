import json
import uuid

from django.test import Client, TestCase


class TaskViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_run_type(self):
        response = self.client.post(
            "/task",
            json.dumps(
                {"Type": "bar", "Value": 10}
            ),
            content_type="application/json",
            HTTP_X_AWS_SQSD_MSGID=uuid.uuid1()
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["result"], 100)

    def test_run_task(self):
        response = self.client.post(
            "/task",
            json.dumps(
                {"Task": "bar", "Value": 10}
            ),
            content_type="application/json",
            HTTP_X_AWS_SQSD_MSGID=uuid.uuid1()
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["result"], 100)

    def test_period_task(self):
        response = self.client.post("/task", "",
                                    content_type="application/json",
                                    HTTP_X_AWS_SQSD_MSGID=uuid.uuid1(),
                                    HTTP_X_AWS_SQSD_TASKNAME="tests.tasks.duck")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["result"], "quack")
