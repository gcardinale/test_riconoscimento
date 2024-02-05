# start app
python3 app.py &
# start redis server
redis-server --daemonize yes &
# start celery worker
celery -A celery_worker.celery worker --loglevel=info --concurrency=1 --pool=solo &
# wait for all processes to finish
wait