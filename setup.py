#!/usr/bin/env python
import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-aws-pubsub',
    version='0.1.0',
    packages=find_packages(),
    python_requires='>=3.7',
    include_package_data=True,
    install_requires=[
        "django>=2.2",
        "boto3>=1.9.181"
    ],
    license='MIT License',  # example license
    test_suite='runtests',
    description='A Django app implement pubsub workers',
    long_description=README,
    url='https://www.example.com/',
    author='Alexander Beach',
    author_email='ajbeach2@gmail.com',
    classifiers=[
        'Environment :: App Environment',
        'Framework :: Django',
        'Framework :: Django :: X.Y',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
