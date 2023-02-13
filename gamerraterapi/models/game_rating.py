from django.db import models

class GameRating(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    player = models.ForeignKey("Player", on_delete=models.SET_NULL, null=True)
    user_rating = models.IntegerField()
    date_rated = models.DateField(auto_now_add=True, null=True, blank=True)
