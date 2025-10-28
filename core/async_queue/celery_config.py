from celery import Celery
import settings
from settings.setting import settings

class Celery_Dependency:
    def __init__(self,
                 broker: str = settings.redis_settings.get_url,
                 backend: str = settings.redis_settings.get_url) -> None:
        self._app = Celery("app", broker=broker, backend=backend)
        self._app.conf.update(
            broker_connection_retry_on_startup=True,
            task_acks_late=True,
            worker_pool='solo',
            worker_concurrency=4,

            imports=["src.apps.auth.tasks"]
        )

    def get_app(self) -> Celery:
        return self._app