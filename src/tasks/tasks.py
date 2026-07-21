from src.tasks.celery_app import celery_instance


@celery_instance.task
def test_task():
    print("task zaversena")
