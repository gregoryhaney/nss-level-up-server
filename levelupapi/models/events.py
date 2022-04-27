from django.db import models

class Event(models.Model):
    game = models.ForeignKey("game", on_delete=models.CASCADE)
    description = models.CharField(max_length=40)
    date = models.DateField
    time = models.TimeField
    organizer = models.ForeignKey("gamer", on_delete=models.CASCADE)
    