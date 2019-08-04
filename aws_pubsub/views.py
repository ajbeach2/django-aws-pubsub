"""aws_pubsub task views."""
import json

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .dispatcher import process


@method_decorator(csrf_exempt, name="dispatch")
class TaskView(View):
    """TaskView to start tasks via REST."""

    def post(self, request):
        task_data = json.loads(request.body)
        recipt_handle, result = process(task_data)

        return JsonResponse({"result": result})
