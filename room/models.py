from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=50)
    profile_picture = models.ImageField(null=True,blank=True)
    desc = models.CharField(max_length=100,null=True,blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    