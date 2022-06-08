from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from books.models import Message


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_user(instance, **kwargs):
    print(f"Signal - '{instance.username}' User authenticated")


@receiver(post_save, sender=Message)
def post_save_message(created, instance, **kwargs):
    instance = instance
    if created:
        print(f"Writer {instance.author} , text is {instance.content}")

