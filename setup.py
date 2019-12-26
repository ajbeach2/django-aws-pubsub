#!/usr/bin/env python
import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-aws-pubsub",
    version="0.1.0",
    packages=["aws_pubsub"],
    python_requires=">=3.8",
    include_package_data=True,
    install_requires=["django>=3.0.1", "boto3"],
    license="MIT License",  # example license
    test_suite="runtests",
    description="A Django app implement pubsub workers",
    long_description=README,
    url="https://github.com/ajbeach2/django-aws-pubsub",
    author="Alexander Beach",
    author_email="ajbeach2@gmail.com",
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :rm: 3.8",
    ],
)
