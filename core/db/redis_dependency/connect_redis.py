from redis import Redis
from settings.setting import settings



class Redis_Dependency:
    def __init__(self):
        try:
            self.redis = Redis(host=settings.redis_settings.redis_host, port=settings.redis_settings.redis_port, db=settings.redis_settings.redis_db)
        except:
            print("Проблем с подключением с redi")
        