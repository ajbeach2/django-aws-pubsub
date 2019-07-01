from django.conf.urls import include
from django.urls import path


urlpatterns = [
    path("task", include("aws_pubsub.urls")),
]
