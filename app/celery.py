from celery import Celery

celery = Celery(
    "tasks", 
    broker="redis://127.0.0.1:6379/0", 
    backend="redis://127.0.0.1:6379/0"
    )



celery.autodiscover_tasks(["app.modules.research"])