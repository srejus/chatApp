from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from home.models import Account
from room.views import *
from room.models import *
from django.contrib.auth import authenticate, login,logout

# Create your views here.
@login_required(login_url='Login')
def index(request):
    return rooms(request)

def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')

        user = authenticate(username=email, password=password)
        if user is not None:
                login(request,user)
                return redirect('/')
        else:
            return Login(request)

    return render(request,'login.html')

def Logout(request):
    logout(request) 
    return redirect('/')

def edit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        pro_pic = request.FILES.get('image')
        about = request.POST.get('about')

        ac = Account.objects.get(user=request.user)
        if(name):
            ac.name = name
        if(pro_pic):
            ac.profile_picture = pro_pic
        if(about):
            ac.desc = about
        
        ac.save()
        return redirect('rooms')

    rooms = Room.objects.all()
    flag = 2

    rooms = Connection.objects.filter(user__user=request.user)
    usr_room = Room.objects.filter(usr2=Account.objects.get(user=request.user))
    
    # Fetch user Account Data
    usrAc = Account.objects.get(user=request.user)

    user_agent = request.META['HTTP_USER_AGENT']

    if 'Mobile' in user_agent:
        return render(request,'mobile/rooms.html',{'rms':rooms})
    return render(request,'room.html',{'rms':rooms,'flag':flag,'ac':usrAc,"rooms":usr_room})
