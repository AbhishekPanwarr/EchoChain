from django.contrib import admin
from .models import User, Conversation, Message

# Register your models here.
class LLMAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "llm_model", "conversation")

admin.site.register(User)
admin.site.register(Conversation)
admin.site.register(Message)