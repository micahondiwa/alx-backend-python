from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Message, Notification, MessageHistory

@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    # Delete all messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete all notifications for the user
    Notification.objects.filter(user=instance).delete()

    # Delete all message histories they edited
    MessageHistory.objects.filter(edited_by=instance).delete()

    # Optionally: delete histories of messages sent by user
    user_messages = Message.objects.filter(sender=instance)
    MessageHistory.objects.filter(message__in=user_messages).delete()
