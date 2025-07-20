from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer

# Conversation ViewSet
class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing and creating conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Limit conversations to those where the user is a participant.
        """
        user = self.request.user
        return Conversation.objects.filter(participants=user).distinct()

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        """
        participants_data = request.data.get('participants', [])
        if not participants_data:
            return Response(
                {"error": "Participants list is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        participants = list(User.objects.filter(user_id__in=participants_data))

        if request.user not in participants:
            participants.append(request.user)  # Ensure creator is added

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ----------------------------
# Message ViewSet
# ----------------------------
class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing and sending messages in a conversation.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Limit messages to a specific conversation and participant.
        """
        conversation_id = self.request.query_params.get('conversation_id')
        user = self.request.user

        if conversation_id:
            return Message.objects.filter(
                conversation__conversation_id=conversation_id,
                conversation__participants=user
            ).order_by('sent_at')
        return Message.objects.none()

    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation.
        """
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body', '').strip()

        if not conversation_id:
            return Response(
                {"error": "Conversation ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not message_body:
            return Response(
                {"error": "Message body cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user not in conversation.participants.all():
            return Response(
                {"error": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
