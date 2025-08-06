from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__first_name', 'participants__last_name', 'participants__email']
    ordering_fields = ['created_at']

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user).distinct()

    def create(self, request, *args, **kwargs):
        participants_data = request.data.get('participants', [])
        if not participants_data:
            return Response({"error": "Participants list is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        participants = list(User.objects.filter(user_id__in=participants_data))
        if request.user not in participants:
            participants.append(request.user)  # ensure creator is included

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['conversation__conversation_id']
    search_fields = ['message_body', 'sender__first_name', 'sender__last_name']
    ordering_fields = ['sent_at']

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        user = self.request.user

        if conversation_id:
            return Message.objects.filter(
                conversation__conversation_id=conversation_id,
                conversation__participants=user
            ).order_by('sent_at')
        return Message.objects.none()

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body', '').strip()

        if not conversation_id:
            return Response({"error": "Conversation ID is required."},
                            status=status.HTTP_400_BAD_REQUEST)
        if not message_body:
            return Response({"error": "Message body cannot be empty."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."},
                            status=status.HTTP_404_NOT_FOUND)

        if request.user not in conversation.participants.all():
            return Response({"error": "You are not a participant in this conversation."},
                            status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
