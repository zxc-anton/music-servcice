import multiprocessing


import multiprocessing

# Количество worker процессов
workers = multiprocessing.cpu_count() * 2 + 1  # Обычная формула
worker_class = "uvicorn.workers.UvicornWorker"
bind = "0.0.0.0:8000"

# Настройки производительности
worker_connections = 1000
max_requests = 10000
max_requests_jitter = 1000
timeout = 120
keepalive = 2

# Логирование
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Перезагрузка
preload_app = True
reload = False