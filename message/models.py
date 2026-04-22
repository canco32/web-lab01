from django.conf import settings
from django.db import models

from chat.models import Chat


class Message(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Чат'
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='Відправник'
    )

    text = models.TextField(
        verbose_name='Текст повідомлення'
    )

    reply_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='Відповідь на повідомлення'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата створення'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата оновлення'
    )

    is_edited = models.BooleanField(
        default=False,
        verbose_name='Редаговано'
    )

    is_deleted = models.BooleanField(
        default=False,
        verbose_name='Видалено'
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Повідомлення'
        verbose_name_plural = 'Повідомлення'
        indexes = [
            models.Index(fields=['chat', 'created_at']),
        ]

    def __str__(self):
        return f"Повідомлення від {self.sender.full_name} у чаті {self.chat}"
