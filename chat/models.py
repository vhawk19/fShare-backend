from email import message
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Room(models.Model):
    created = models.DateTimeField(auto_now_add=True,editable=False)
    name = models.TextField(default='NA')
    room_id =models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User)
    # admins = models.ManyToManyField(User)

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_id=models.ForeignKey(Room,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,editable=False)
    text = models.TextField(null=True)
    magnet_uri = models.TextField(null=True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)