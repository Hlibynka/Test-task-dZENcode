from celery import shared_task
import time

@shared_task
def process_new_comment_task(comment_id):
    time.sleep(5)
    print(f"Фонова задача виконана! Коментар {comment_id} успішно оброблено.")
    return True