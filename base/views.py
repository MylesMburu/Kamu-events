from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Event
from .forms import EventForm

# events = [
#     {'id': 1 , 'name':'Data science I4G'},
#     {'id': 2 , 'name':'Cyber Security I4G'},

# ]

# Create your views here.
def home(request):
    events = Event.objects.all()
    context = {'events': events}
    # events = Event.objects.all()
    return render(request, 'base/home.html',context)

def event(request, pk):
    event = Event.objects.get(id=pk)
    context = {'event': event}   

    return render(request,'base/event.html', context)

def createEvent(request):
    if request.method == 'POST':  #getting the POST request from the form
        form = EventForm(request.POST)
        if form.is_valid:
            form.save()     #saves the data from the form in the database
            return redirect('home')
    form = EventForm()
    context = {'form': form}
    return render (request,'base/event_form.html', context)

def updateEvent(request, pk):
    event = Event.objects.get(id=pk)
    form = EventForm(instance=event)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid:
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/event_form.html', context)

def deleteEvent(request, pk):
    event = Event.objects.get(id=pk)

    if request.method == 'POST':
        event.delete()
        return redirect('home')

    context = {'obj':event}
    return render(request, 'base/delete.html', context)    