from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} by {self.user.username}"

    class Meta:
        db_table = 'conversation'
        managed = True
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    llm_model= models.CharField(max_length=10, choices=[("deepseek", "DeepSeek"), ("gemini", "Gemini"), ("claude", "Claude"), ("sota", "SOTA")])
    sender = models.CharField(max_length=10, choices=[('user', 'User'), ('assistant', 'Assistant')])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.id}:  {self.sender.capitalize()} at {self.timestamp}: {self.content[:30]}"

    class Meta:
        db_table = 'message'
        managed = True
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'