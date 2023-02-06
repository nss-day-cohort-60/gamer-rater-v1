from django.db import models

class GamePhoto(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='game_photos')
    player = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='player_photos')
    photo_url = models.CharField()
    date_added = models.DateTimeField()
