from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Tasks(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Posted at")
    content = models.TextField()
    year = models.IntegerField()
    month = models.IntegerField()
    date = models.IntegerField()
    hour = models.IntegerField()
    minute = models.IntegerField()
    completed = models.BooleanField(default= False)

    def __str__(self):
        return f"{self.content}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "year": self.year,
            "month": self.month,
            "date": self.date,
            "hour": self.hour,
            "minute": self.minute,
            "completed": self.completed,
        }    