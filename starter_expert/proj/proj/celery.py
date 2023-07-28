import os
from celery.schedules import crontab
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('proj')
app.conf.enable_utc = False

app.conf.update(timezone='Europe/Moscow')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'create-reports-every-day': {
        'task': 'services.tasks.iterateNmids',
        'schedule': crontab(hour=9, minute=30),
    },
    'clear-old-seo-collectors': {
        'task': 'services.tasks.clear_old_seo_collectors',
        'schedule': crontab(hour=7, minute=59),
    }
}





# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')