from redis import Redis
from settings.setting import settings


class Redis_Dependency:
    def __init__(self, host: str = settings.redis_settings.redis_host,
                 port: int = settings.redis_settings.redis_port,
                 db: int = settings.redis_settings.redis_db) -> None:
        self._redis = Redis(
            host=host,
            port=port,
            db=db
        )