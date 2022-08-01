from django.db import models
from django.contrib.auth.models import User

from home.models import Account

class Room(models.Model):
    name = models.CharField(max_length=50)
    profile_picture = models.ImageField(null=True,blank=True)
    desc = models.CharField(max_length=100,null=True,blank=True)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="usderID")

    isPrivate = models.BooleanField(default=False)
    usr1 = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='user1',null=True,blank=True)
    usr2 = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='user2',null=True,blank=True)

    def __str__(self):
        return str(self.name)
    
class Message(models.Model):
    room = models.ForeignKey(Room,related_name="messages",on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name="usr",on_delete=models.CASCADE)
    content = models.TextField(null=True,blank=True)
    time_added = models.DateTimeField(auto_now_add=True)

    def get_len(self):
        return len(self.content)

    class Meta:
        ordering = ('time_added',)


class Connection(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='room')
    user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='account')