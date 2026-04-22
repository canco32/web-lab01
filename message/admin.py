from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['chat', 'sender', 'is_deleted', 'created_at']
    list_filter = ['is_deleted', 'created_at']
    search_fields = ['text', 'sender__email']
    actions = ['mark_deleted', 'mark_restored']

    def mark_deleted(self, request, queryset):
        queryset.update(is_deleted=True)
    mark_deleted.short_description = "Позначити як видалені"

    def mark_restored(self, request, queryset):
        queryset.update(is_deleted=False)
    mark_restored.short_description = "Відновити вибрані"
