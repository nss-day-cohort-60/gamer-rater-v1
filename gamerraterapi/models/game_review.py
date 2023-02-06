from django.db import models

class GameReview(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='player_reviews')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='game_reviews')
    review = models.CharField(max_length=700)
    date_reviewed = models.DateTimeField()
