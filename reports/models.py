from django.db import models
from django.conf import settings

class Station(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    observers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="stations", blank=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="messages")
    observer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.station} – {self.observer} @ {self.created_at}"
