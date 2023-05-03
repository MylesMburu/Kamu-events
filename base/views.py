from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Event, Topic
from .forms import EventForm

# events = [
#     {'id': 1 , 'name':'Data science I4G'},
#     {'id': 2 , 'name':'Cyber Security I4G'},

# ]

# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:   # stops a logged in user from logging in again
        return redirect('home')
    
    if request.method =='POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username) # checks whether the username entered in theform exists in the database
        except:
            if password == '':
                messages.error(request, 'Password cannot be blank')
    
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'Wrong username or password!')
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()

    if request.method == 'post':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('login')
        else:
            messages.error(request, 'There seems to be an error in the registration process')
    return render(request, 'base/login_register.html', {'form':form})

def home(request):
    events = Event.objects.all()
    topics = Topic.objects.all()

    q = request.GET.get('q') if request.GET.get('q') != None else '' #variable to query
    events = Event.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(host__username__icontains=q)) #Filters the events according to the topic name

    event_count = events.count()
    context = {'events': events, 'topics':topics, 'event_count':event_count}
    # events = Event.objects.all()
    return render(request, 'base/home.html',context)

def event(request, pk):
    event = Event.objects.get(id=pk)
    context = {'event': event}   

    return render(request,'base/event.html', context)

@login_required(login_url='login')
def createEvent(request):
    if request.method == 'POST':  #getting the POST request from the form
        form = EventForm(request.POST)
        if form.is_valid:
            event = form.save(commit=False)  # Don't save the form to the database yet
            event.host = request.user  # Set the host to the current user
            form.save()     #saves the data from the form in the database
            return redirect('home')
    form = EventForm()
    context = {'form': form}
    return render (request,'base/event_form.html', context)

@login_required(login_url='login')
def updateEvent(request, pk):
    event = Event.objects.get(id=pk)
    form = EventForm(instance=event)

    if request.user != event.host:  # prevents a user from editing an event that is not theirs
        return HttpResponse('This is not your event!')
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid:
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/event_form.html', context)

@login_required(login_url='login')
def deleteEvent(request, pk):
    event = Event.objects.get(id=pk)

    if request.user != event.host:  #prevents a user from deleting an event that is not theirs
        return HttpResponse('This is not your event!')
    
    if request.method == 'POST':
        event.delete()
        return redirect('home')

    context = {'obj':event}
    return render(request, 'base/delete.html', context)    