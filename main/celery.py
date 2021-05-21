from __future__ import absolute_import, unicode_literals

import os
import environ

from celery import Celery

env = environ.Env()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', env.str("DJANGO_SETTINGS_MODULE", default='main.settings.production'))

celery_app = Celery('main', namespace='CELERY')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
