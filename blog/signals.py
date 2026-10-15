
import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Post


@receiver(post_delete, sender=Post)
def delete_post_image(sender, instance, **kwargs):
    if instance.cover_image:
        image_path = instance.cover_image.path

        if os.path.isfile(image_path):
            os.remove(image_path)
