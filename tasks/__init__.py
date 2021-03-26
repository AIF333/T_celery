
# celery -A hdy_celery.hdy_celery worker -Q user_quick,user_normal,user_large -P eventlet
# celery -A hdy_celery.hdy_celery worker -Q user_quick -P eventlet
# celery -A hdy_celery.hdy_celery worker -Q user_normal -P eventlet
# celery -A hdy_celery.hdy_celery worker -Q user_large -P eventlet


# celery -A hdy_celery.hdy_celery worker -Q inner_quick,inner_normal,inner_large -P eventlet
# celery -A hdy_celery.hdy_celery worker -Q inner_quick -P eventlet
# celery -A hdy_celery.hdy_celery worker -Q inner_normal -P eventlet
# celery -A hdy_celery.hdy_celery worker -Q inner_large -P eventlet


