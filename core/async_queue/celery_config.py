from celery import Celery
from settings.setting import settings


app = Celery("app", broker=settings.redis_settings.get_url, backend=settings.redis_settings.get_url)
app.conf.update(
    broker_connection_retry_on_startup=True,
    task_acks_late=True,
    worker_pool='solo',
    worker_concurrency=4,

    imports=["src.apps.auth.tasks"]
)