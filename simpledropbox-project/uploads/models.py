from django.db import models

# Create your models here.

class Upload(models.Model):
    f = models.FileField(upload_to='dropbox/')
