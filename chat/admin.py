from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'original_text', 'translated_text', 'timestamp')
    readonly_fields = ('timestamp',)
