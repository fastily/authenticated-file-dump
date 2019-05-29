from django.db import models
from django.contrib.auth.models import User # django's builtin User model


import uuid

class Upload(models.Model):
    f = models.FileField(upload_to='dropbox/')
    date = models.DateTimeField()
    u = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4)
