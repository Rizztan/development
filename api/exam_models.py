# api/exam_models.py
from django.db import models
from django.utils import timezone

class Chat(models.Model):
    username = models.CharField(max_length=100)
    chat_message = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.username}: {self.chat_message[:50]}"
