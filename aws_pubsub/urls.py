"""aws_pubsub task url."""

from aws_pubsub import views
from django.urls import path

app_name = "aws_pubsub"

urlpatterns = [
    path("", views.TaskView.as_view(), name="task"),
]
