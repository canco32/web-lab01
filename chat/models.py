from django.conf import settings
from django.db import models


class Chat(models.Model):
    CHAT_TYPES = [
        ('private', 'Приватний'),
        ('group', 'Груповий')
    ]

    type = models.CharField(max_length=20, choices=CHAT_TYPES, default='private')
    title = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='chat_created_by',
        verbose_name='Автор'
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ChatMember',
        related_name='Чати',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.type == 'group':
            return self.title or f"Груповий чат #{self.id}"
        return f"Приватний чат #{self.id}"


class ChatMember(models.Model):
    CHAT_ROLE_CHOICES = [
        ('admin', 'Адміністратор'),
        ('member', 'Учасник'),
        ('owner', 'Власник'),
    ]

    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name='Чат',
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_memberships',
        verbose_name='Користувач',
    )

    role = models.CharField(
        max_length=20,
        choices=CHAT_ROLE_CHOICES,
        default='member',
        verbose_name='Роль',
    )

    joined_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата приєднання',
    )

    last_read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Останнє прочитане',
    )

    is_muted = models.BooleanField(
        default=False,
        verbose_name='Сповіщення вимкнено',
    )

    class Meta:
        unique_together = ('chat', 'user')
        verbose_name = 'Учасник чату'
        verbose_name_plural = 'Учасники чатів'

    def __str__(self):
        return f"{self.user.full_name} у чаті {self.chat}"
