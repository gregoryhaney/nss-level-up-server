from django.db import models

class Game(models.Model):
    game_type = models.ForeignKey("game_type", on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    maker = models.CharField(max_length=25)
    gamer = models.ForeignKey("gamer", on_delete=models.CASCADE)
    number_of_players = models.IntegerField
    skill_level = models.IntegerField
    