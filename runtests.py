#!/usr/bin/env python

"""Test Runnger for aws_pubsub."""
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ in ["__main__", "runtests"]:
    if len(sys.argv) > 1:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv)
    else:
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"
        django.setup()
        TestRunner = get_runner(settings)
        test_runner = TestRunner()
        failures = test_runner.run_tests(["tests"])
        sys.exit(bool(failures))
