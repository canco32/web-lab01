from django.contrib import admin

from .models import Chat, ChatMember


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'created_by', 'is_active', 'created_at']
    list_filter = ['type', 'created_at', 'created_by']
    search_fields = ['title']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(ChatMember)
class ChatMemberAdmin(admin.ModelAdmin):
    list_display = ['chat', 'user', 'role', 'joined_at']
    list_filter = ['role', 'joined_at']
    search_fields = ['user__email', 'chat__title']
