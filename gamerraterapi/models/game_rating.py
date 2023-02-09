from django.db import models

class GameRating(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    player = models.ForeignKey("Player", on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField()
    date_rated = models.DateField(auto_now=True)
