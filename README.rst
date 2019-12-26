=====
Aws Pubsub
=====

AwsPubsub is a  Django app for asyncronous background tasks leverageing SQS. AwsPubSub also supports Elastic Beanstalk Worker environments.

|B| |R| |L| |M| |C|

.. |B| image:: https://circleci.com/gh/ajbeach2/django-aws-pubsub.svg?style=svg
    :target: https://circleci.com/gh/ajbeach2/django-aws-pubsub
.. |R| image:: https://img.shields.io/github/release/ajbeach2/django-aws-pubsub.svg
   :alt: Latest Release
.. |L| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :alt: Latest Release
.. |M| image:: https://api.codeclimate.com/v1/badges/880cc54a4c2c8bbd00bd/maintainability
   :target: https://codeclimate.com/github/ajbeach2/django-aws-pubsub/maintainability
   :alt: Maintainability
.. |C| image:: https://codecov.io/gh/ajbeach2/django-aws-pubsub/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/ajbeach2/django-aws-pubsub
   
 

Quick start
-----------

1. Add "aws_pubsub" to your INSTALLED_APPS setting.

.. code:: python

	INSTALLED_APPS = [
	    ...
	    "aws_pubsub",
	]

2. Configure your sqs queue and (optionally) set the sns topic in settings.py. The topic and queue will be created if they do not exists. The queue will subscribe to the topic by default. See `boto3 <https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html>`_ for details on setting up credentials with AWS

.. code:: python
	
	WORKER_CONFIG = {
		"QUEUE_NAME": "worker-queue",
		"TOPIC_NAME": "worker-topic"
	}


3. Create Tasks in a tasks.py file in your Django app and register them. Optionally pass a global alias for the task.

.. code:: python

	from aws_pubsub import register

	def foo(message: dict):
	    print("fooooooooooooooooooooooo")

	def bar(message: dict):
	    value = message["Value"]
	    return value * 10

	register(foo, alias="foo")
	register(bar)


4. Enqueue your tasks. To enqueue a task, use the global alias or the absolute module path.  A delay in seconds my also be passed

.. code:: python

	from aws_pubsub import send_task

	send_task("foo", {})
	send_task("myapp.tasks.bar", {"Value": 10}, delay=10)


5. Run tasks sync from a REST endpoint. This is compatible with `AWS Elasticbean Stalk Worker Environments <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features-managing-env-tiers.html>`_. Add the following to your urls.py. Note: This route is unauthenticated and disables CSRF tokens.

.. code:: python

	urlpatterns = [
		...
    		path("task", include("aws_pubsub.urls")),
	]

6. Running Task Worker from the command line

workers argument defaults to number of cpu * 2. You may pass in a value for workers to set the desired concurrency

.. code:: bash

	python manage.py runworker --workers 8
