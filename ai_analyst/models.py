from django.db import models
from django.conf import settings
from users.models import User

# Create your models here.
class AISummary(models.Model):
    user = models.ForeignKey( settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ai_summary = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

