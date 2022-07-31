from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    name = models.CharField(max_length=100,null=True,blank=True)
    profile_picture = models.ImageField(null=True,blank=True,upload_to='user_profile')
    desc = models.CharField(max_length=150,null=True,blank=True)

    def __str__(self):
        return self.name

