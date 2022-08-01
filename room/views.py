from django.shortcuts import render
from django.contrib.auth.models import User

from room.models import Connection, Message, Room
from home.models import Account

# Create your views here.
def rooms(request):
    rooms = Connection.objects.filter(user__user=request.user)
    usrAc = Account.objects.get(user=request.user)
    flag = 0

    user_agent = request.META['HTTP_USER_AGENT']

    if 'Mobile' in user_agent:
        return render(request,'mobile/rooms.html',{'rms':rooms})
    return render(request,'room.html',{'rms':rooms,'flag':flag,'ac':usrAc})


def room(request,slug):
    try:
        room = Room.objects.get(slug=slug)
        rooms = Room.objects.all()
        usrAc = Account.objects.get(user=request.user)

        # fetch all messages saved on the database
        messages = Message.objects.filter(room=room)[0:25]
        flag = 1

        
        # Check if private
        if room.isPrivate == True:
            print("Working")
            if room.usr1.user == request.user:
                me = Account.objects.get(user=room.usr1.user)
                other = Account.objects.get(user=room.usr2.user)
                print("ME: ",me.name)
                print("OTHER: ",other.name)
                print("LOGED IN: ",request.user)
            else:
                print("ELSE")
                other = Account.objects.get(user=room.usr1.user)
                me = Account.objects.get(user=room.usr2.user)
                print("ME: ",me.name)
                print("OTHER: ",other.name)
                print("LOGED IN: ",request.user)
               
            
            return render(request,'room.html',{'rms':rooms,'flag':flag,'room':room,'messages':messages,'ac':usrAc,"me":me,"other":other})
        user_agent = request.META['HTTP_USER_AGENT']

        if 'Mobile' in user_agent:
            return render(request,'mobile/room.html',{'room':room})
        return render(request,'room.html',{'rms':rooms,'flag':flag,'room':room,'messages':messages,'ac':usrAc})
    except:
        print("EXCEPT")
        rooms = Room.objects.all()
        usrAc = Account.objects.get(user=request.user)
        flag = 0

        user_agent = request.META['HTTP_USER_AGENT']

        if 'Mobile' in user_agent:
            return render(request,'mobile/rooms.html',{'rms':rooms})
        return render(request,'room.html',{'rms':rooms,'flag':flag,'ac':usrAc})


def chat_setting(request,slug):
    usrAc = Account.objects.get(user=request.user)
    room = Room.objects.get(slug=slug)
    rooms = Room.objects.all()

    return render(request,'room.html',{'rms':rooms,'flag':3,'room':room,'ac':usrAc})

def clear_chat(request,slug):
    # fetch all messages from database
    x = Message.objects.filter(room__slug = slug)
    x.delete()
    return room(request,slug)

def delete_group(request,slug):
    x = Room.objects.get(slug=slug)
    x.delete()
    return rooms(request)

def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        about = request.POST.get('about')
        image = request.FILES.get('image')

        slug = "".join(name.split())

        if(image):
            x = Room(name=name,profile_picture=image,desc=about,slug=slug.lower(),owner = request.user)
            x.save()
        else:
            x = Room(name=name,desc=about,slug=slug.lower(),owner = request.user)
            x.save()

            x.slug += str(x.id)
            x.save()
        
        return rooms(request)

