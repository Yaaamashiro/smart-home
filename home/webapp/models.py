from django.db import models

class InfraredSignal(models.Model):
    name = models.CharField(max_length=20, unique=True)
    content = models.TextField()