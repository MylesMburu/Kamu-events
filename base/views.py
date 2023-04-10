from django.shortcuts import render
from django.http import HttpResponse
from .models import Event

events = [
    {'id': 1 , 'name':'Data science I4G'},
    {'id': 1 , 'name':'Cyber Security I4G'},

]

# Create your views here.
def home(request):
    context = {'events': events}
    # events = Event.objects.all()
    return render(request, 'base/home.html',context)

def event(request):
    return render(request,'base/event.html')
