from django.shortcuts import render
from django.contrib.auth.models import User

from room.models import Connection, Message, Room
from home.models import Account

# Create your views here.
def rooms(request):
    rooms = Connection.objects.filter(user__user=request.user)

    usr_room = Room.objects.filter(usr2=Account.objects.get(user=request.user))
    usrAc = Account.objects.get(user=request.user)
    flag = 0

    user_agent = request.META['HTTP_USER_AGENT']

    if 'Mobile' in user_agent:
        return render(request,'mobile/rooms.html',{'rms':rooms})
    return render(request,'room.html',{'rms':rooms,'flag':flag,'ac':usrAc,"rooms":usr_room})

def search(request):
    term = request.GET.get('term')
    room = Room.objects.filter(slug__contains=term)
    usrs = Account.objects.filter(name__contains = term)

    usrAc = Account.objects.get(user=request.user)
    flag = 4

    return render(request,'room.html',{'rooms':room,'flag':flag,'ac':usrAc,'usrs':usrs})



def room(request,slug):
        if(Room.objects.filter(slug=slug).exists()):
            room = Room.objects.get(slug=slug)
        else:
            # It is a user

            me = Account.objects.get(user=request.user)
            other = Account.objects.get(user__username=slug)

            usr_slug = str(request.user.username)+'-'+str(slug)
            usr_slug_rev = str(slug)+'-'+str(request.user.username)
            if(Room.objects.filter(slug=usr_slug).exists()):
                room = Room.objects.get(slug=usr_slug)
            elif(Room.objects.filter(slug=usr_slug_rev).exists()):
                room = Room.objects.get(slug=usr_slug_rev)
            else:
                usr = Room(name=slug,slug=usr_slug,isPrivate=True,usr1=me,usr2=other,owner=request.user)
                usr.save()

                room = Room.objects.get(slug=usr_slug)
        # Check if the room already connected or not
        me_usr = Account.objects.get(user=request.user)
        if(Connection.objects.filter(room=room,user=me_usr).count() == 0):
            x = Connection(room=room,user=me_usr)
            x.save()

        rooms = Connection.objects.filter(user=me_usr)
        usrAc = Account.objects.get(user=request.user)
        usr_room = Room.objects.filter(usr2=Account.objects.get(user=request.user))

        # fetch all messages saved on the database
        messages = Message.objects.filter(room=room)[0:25]
        flag = 1

        
        # Check if private
        if room.isPrivate == True:
            if room.usr1.user == request.user:
                me = Account.objects.get(user=room.usr1.user)
                other = Account.objects.get(user=room.usr2.user)
                
            else:
                print("ELSE")
                other = Account.objects.get(user=room.usr1.user)
                me = Account.objects.get(user=room.usr2.user)
  
            return render(request,'room.html',{'rms':rooms,'flag':flag,'room':room,'messages':messages,'ac':usrAc,"me":me,"other":other,"rooms":usr_room})
        user_agent = request.META['HTTP_USER_AGENT']

        if 'Mobile' in user_agent:
            return render(request,'mobile/room.html',{'room':room})
        return render(request,'room.html',{'rms':rooms,'flag':flag,'room':room,'messages':messages,'ac':usrAc,"rooms":usr_room})
   

def chat_setting(request,slug):
    usrAc = Account.objects.get(user=request.user)
    room = Room.objects.get(slug=slug)
    rooms = Connection.objects.filter(user__user=request.user)
    usr_room = Room.objects.filter(usr2=Account.objects.get(user=request.user))

    members = Connection.objects.filter(room=room)

    return render(request,'room.html',{'rms':rooms,'flag':3,'room':room,'ac':usrAc,"rooms":usr_room,'mem':members})

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

        me_usr = Account.objects.get(user=request.user)

        if(image):
            x = Room(name=name,profile_picture=image,desc=about,slug=slug.lower(),owner = request.user)
            x.save()

            x.slug += str(x.id)
            x.save()

            # Create connections for this
            
            c = Connection(room=x,user=me_usr)
            c.save()

        else:
            x = Room(name=name,desc=about,slug=slug.lower(),owner = request.user)
            x.save()

            x.slug += str(x.id)
            x.save()

            # Create connections for this

            c = Connection(room=x,user=me_usr)
            c.save()
        

        
        return rooms(request)

