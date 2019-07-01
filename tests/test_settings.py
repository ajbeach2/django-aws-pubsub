from __future__ import unicode_literals, absolute_import
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
    }
}

SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    "tests",
]
