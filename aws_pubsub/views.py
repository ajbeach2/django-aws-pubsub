"""aws_pubsub task views."""
import json

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .dispatcher import process_task


@method_decorator(csrf_exempt, name="dispatch")
class TaskView(View):
    """TaskView to start tasks via REST."""

    def post(self, request):
        # Means this is a periodic task, which will have an empty body
        if 'HTTP_X_AWS_SQSD_TASKNAME' in request.META:
            task_data = {
                "Type": request.META["HTTP_X_AWS_SQSD_TASKNAME"]
            }
        else:
            task_data = json.loads(request.body)

        result, _ = process_task(task_data)

        return JsonResponse({"result": result})
