from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_redis import get_redis_connection

from .models import Task


@receiver([post_save, post_delete], sender=Task)
def reset_cache_after_task_changed(sender, instance, **kwargs):
    redis = get_redis_connection("default")

    pattern = f"*:task_list:{instance.user_id}:*"

    for key in redis.scan_iter(match=pattern):
        redis.delete(key)
