worker: celery -A mainApp.celery worker -B -l info -E concurrency 2

web: gunicorn StockWatcher.wsgi

