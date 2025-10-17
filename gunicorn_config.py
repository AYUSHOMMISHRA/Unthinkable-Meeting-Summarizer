import os
import multiprocessing

# Bind to Railway's PORT or default to 8080
bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"

# Worker configuration
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 300
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
