from django.db import models
from django.utils import timezone
from .user import Users

class Community_forum(models.Model):
    commented_by=models.ForeignKey(Users, on_delete=models.CASCADE)
    comment=models.TextField(verbose_name="Comment")
    created=models.DateTimeField(default=timezone.now)
    updated=models.DateTimeField(auto_now=True)

