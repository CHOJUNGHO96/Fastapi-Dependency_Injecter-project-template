import json
import multiprocessing
import os

host = "0.0.0.0"
port = "5051"
bind = f"{host}:{port}"

# 기존 설정 유지
workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
cores = multiprocessing.cpu_count()
workers_per_core = float(workers_per_core_str)
workers = max(int(workers_per_core * cores), 2)

# 로그, 타임아웃, keepalive 설정
loglevel = os.getenv("LOG_LEVEL", "info")
accesslog = os.getenv("GUNICORN_ACCESS_LOG", "-")
errorlog = os.getenv("GUNICORN_ERR_LOG", "-")
graceful_timeout = int(os.getenv("GRACEFUL_TIMEOUT", "120"))
timeout = int(os.getenv("TIMEOUT", "120"))
keepalive = int(os.getenv("KEEP_ALIVE", "5"))

# 구니콘 설정 변수
gunicorn_config = {
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    "accesslog": accesslog,
    "errorlog": errorlog,
    "graceful_timeout": graceful_timeout,
    "timeout": timeout,
    "keepalive": keepalive,
}

print(json.dumps(gunicorn_config))
