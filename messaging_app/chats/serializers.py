from rest_framework import serializers
from .models import User, Conversation, Message


# ----------------------------
# User Serializer
# ----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at',
        ]
        read_only_fields = ['user_id', 'created_at']


# ----------------------------
# Conversation Serializer
# ----------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
        ]
        read_only_fields = ['conversation_id', 'created_at']


# ----------------------------
# Message Serializer
# ----------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'conversation',
            'message_body',
            'sent_at',
        ]
        read_only_fields = ['message_id', 'sent_at', 'sender']
