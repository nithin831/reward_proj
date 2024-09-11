# rewards/models.py
from django.db import models
from django.contrib.auth.models import User

class App(models.Model):
    name = models.CharField(max_length=100)
    download_link = models.URLField()
    points = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to='screenshots/')
    completed = models.BooleanField(default=False)
    points_earned = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.app.name}"
