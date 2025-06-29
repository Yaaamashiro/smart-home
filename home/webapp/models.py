from django.db import models

class InfraredSignal(models.Model):
    name = models.CharField(max_length=20, unique=True)
    content = models.TextField()

class Lock(models.Model):
    is_opened = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
