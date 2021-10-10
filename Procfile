worker: celery -A mainApp.celery worker -B -l info -E -O fair --without-gossip --without-mingle --without-heartbeat --concurrency=4

web: gunicorn StockWatcher.wsgi

