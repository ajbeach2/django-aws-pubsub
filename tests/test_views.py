import json

from django.test import Client, TestCase


class TaskViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_run_task(self):
        response = self.client.post(
            "/task",
            json.dumps({
                "MessageId": "bfba876e-d84b-4a81-ad25-ac044685bf90",
                "Body": '{"Type": "bar", "Value":10}'
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["result"], 100)
