from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from chat.models import Chat
from message.models import Message

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Серіалізатор для реєстрації користувача"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'gender', 'birth_date', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Паролі не співпадають")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """Серіалізатор для входу користувача"""
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Невірний email або пароль')
            if not user.is_active:
                raise serializers.ValidationError('Акаунт деактивовано')
            data['user'] = user
        else:
            raise serializers.ValidationError('Необхідно вказати email та пароль')

        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """Серіалізатор для профілю користувача"""
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'full_name',
                  'gender', 'birth_date', 'avatar', 'bio', 'created_at']
        read_only_fields = ['id', 'email', 'created_at']


class ChatSerializer(serializers.ModelSerializer):
    """Серіалізатор для чатів"""
    created_by = UserProfileSerializer(read_only=True)
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'type', 'title', 'created_by', 'is_active', 'members_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def get_members_count(self, obj):
        return obj.members.count()


class MessageSerializer(serializers.ModelSerializer):
    """Серіалізатор для повідомлень"""
    author = UserProfileSerializer(source='sender', read_only=True)
    replies = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'chat', 'author', 'reply_to', 'text', 'is_deleted', 'replies', 'can_edit',
                  'created_at', 'updated_at', 'is_edited']
        read_only_fields = ['id', 'author', 'is_edited', 'is_deleted', 'created_at', 'updated_at']

    def get_replies(self, obj):
        if obj.replies.exists():
            return MessageSerializer(
                obj.replies.filter(is_deleted=False),
                many=True,
                context=self.context
            ).data
        return []

    def get_can_edit(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.sender == request.user or request.user.is_staff
        return False

    def validate(self, data):
        request = self.context.get('request')
        chat = data.get('chat') or (self.instance.chat if self.instance else None)
        if chat and request and request.user.is_authenticated:
            if not chat.participants.filter(pk=request.user.pk).exists():
                raise serializers.ValidationError('Немає доступу до цього чату')
        return data
