from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from chat.models import Chat, ChatMember
from message.models import Message
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    ChatSerializer,
    MessageSerializer,
)


class UserRegistrationView(generics.CreateAPIView):
    """
    Реєстрація нового користувача в системі.

    Створює новий акаунт користувача з обов'язковими полями:
    - email (унікальний)
    - username
    - first_name
    - last_name
    - password, password_confirm

    Опціональні поля:
    - gender
    - birth_date
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    """Вхід користувача"""
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key
        })


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Профіль користувача"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChatListView(generics.ListAPIView):
    """Список чатів"""
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(
            is_active=True,
            participants=self.request.user
        ).select_related('created_by').distinct()


class ChatDetailView(generics.RetrieveAPIView):
    """Деталі чату"""
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(
            is_active=True,
            participants=self.request.user
        ).select_related('created_by').distinct()


class MessageListCreateView(generics.ListCreateAPIView):
    """Список та створення повідомлень"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        chat_id = self.request.query_params.get('chat')
        if not chat_id:
            return Message.objects.none()
        if not self.request.user.is_authenticated:
            return Message.objects.none()
        if not ChatMember.objects.filter(chat_id=chat_id, user=self.request.user).exists():
            return Message.objects.none()
        return Message.objects.filter(
            chat_id=chat_id,
            is_deleted=False,
            reply_to=None
        ).select_related('sender', 'chat').prefetch_related('replies__sender')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Деталі, оновлення та видалення повідомлення"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def app_info_view(request):
    """Інформація про додаток"""
    emblem_path = f'{settings.STATIC_URL}emblem.png'
    if not emblem_path.startswith('/'):
        emblem_path = '/' + emblem_path
    return Response({
        'name': 'Real Chat',
        'emblem': request.build_absolute_uri(emblem_path),
        'version': '1.0.0',
        'description': 'Чат з приватними та груповими розмовами та повідомленнями',
        'features': [
            'Реєстрація та авторизація користувачів',
            'Перегляд чатів',
            'Обмін повідомленнями',
            'Відповіді на повідомлення',
        ],
        'author': 'Сілін Ілля Денисович',
        'contact': '@IicancoI'
    })
