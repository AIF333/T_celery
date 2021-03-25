
# celery -A hdy_celery.hdy_celery worker -Q user_quick,user_normal,user_large -P eventlet
# celery -A hdy_celery.hdy_celery worker -Q user_large -P eventlet
