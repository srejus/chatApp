from django.shortcuts import render

from room.models import Room

# Create your views here.
def rooms(request):
    rooms = Room.objects.all()
    flag = 0

    user_agent = request.META['HTTP_USER_AGENT']

    if 'Mobile' in user_agent:
        return render(request,'test.html')
    return render(request,'room.html',{'rms':rooms,'flag':flag})

def room(request,slug):
    room = Room.objects.get(slug=slug)
    rooms = Room.objects.all()
    flag = 1
    return render(request,'room.html',{'rms':rooms,'flag':flag,'room':room})
