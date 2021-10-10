worker: celery -A mainApp.celery worker -l info -O fair --without-gossip --without-mingle --without-heartbeat --concurrency=4

web: gunicorn StockWatcher.wsgi

