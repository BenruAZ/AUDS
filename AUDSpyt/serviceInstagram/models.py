from django.db import models

# Create your models here.
class PostFoto(models.Model):
    nombre = models.CharField(max_length=250)