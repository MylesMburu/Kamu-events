from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'base/home.html')

def body(request):
    return render(request,'base/body.html')
