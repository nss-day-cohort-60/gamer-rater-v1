from django.db import models

class GameRating(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='player_ratings')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='game_ratings')
    rating = models.IntegerField()
    date_rated = models.DateTimeField()