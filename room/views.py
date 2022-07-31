from django.shortcuts import render

from room.models import Room

# Create your views here.
def rooms(request):
    rooms = Room.objects.all()
    return render(request,'rooms.html',{'rms':rooms})

def room(request,slug):
    rooms = Room.objects.get(slug=slug)
    return render(request,'room.html',{'rms':rooms})
