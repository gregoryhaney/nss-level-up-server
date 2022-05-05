from django.db import models

class Event(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    description = models.CharField(max_length=40)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    attendees = models.ManyToManyField("Gamer", through="EventGamer", related_name="events")
    
    # DateField is a class and requires empty parenthesis at the end
    # DateField must be in YYYY-MM-DD format
    # TimeField is a class and requires empty parenthesis at the end
    # TimeField must be in HH:MM[:ss[.uuuuuu]] format.

    @property
    def joined(self):
        return self.__joined
    
    @joined.setter
    def joined(self, value):
        self.__joined = value
        
        