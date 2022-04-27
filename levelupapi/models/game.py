from django.db import models

class Game(models.Model):
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    maker = models.CharField(max_length=25)
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    number_of_players = models.IntegerField()
    skill_level = models.IntegerField()
    
    
    
    # IntegerField is a class, so it requires empty parenthesis at the end