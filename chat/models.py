from django.db import models

from users.models import User


class Room(models.Model):
    name = models.CharField(null=True, default=None, max_length=90)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RoomMember(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    unread_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RoomMessage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    member = models.ForeignKey(RoomMember, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
