from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # Threaded conversation support
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    # Edit tracking
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="edited_messages")

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:30]}"


# Optional helper to fetch threaded replies

def get_threaded_messages(message):
    """
    Recursively get all replies to a message.
    Returns a list of dictionaries containing message and nested replies.
    """
    thread = []
    for reply in message.replies.all():
        thread.append({
            'message': reply,
            'replies': get_threaded_messages(reply)
        })
    return thread


# Example ORM query optimization in your views or logic

def fetch_top_level_messages():
    messages = Message.objects.filter(parent_message__isnull=True).select_related(
        'sender', 'receiver'
    ).prefetch_related(
        'replies__sender', 'replies__receiver'
    )
    return messages
