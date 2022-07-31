from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=50)
    profile_picture = models.ImageField(null=True,blank=True)
    slug = models.SlugField(unique=True)