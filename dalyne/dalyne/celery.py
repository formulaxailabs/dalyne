from __future__ import absolute_import
import os
from celery import Celery


# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dalyne.settings')

app = Celery('dalyne')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
