from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Event(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):    #A child model of the Event model
    # user =
    event = models.ForeignKey(Event, on_delete=models.CASCADE)    #identifies the fk which is the pk of the parent(Event). This model is deleted if the parent is also deleted
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]
    