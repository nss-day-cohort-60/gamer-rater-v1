from django.db import models

class GamePhoto(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    player = models.ForeignKey("Player", on_delete=models.SET_NULL, null=True)
    photo_url = models.CharField(max_length=248)
    date_added = models.DateField(auto_now=True)
