from django.db import models

class Game(models.Model):
    player = models.ForeignKey("Player", on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=48)
    description = models.CharField(max_length=2048)
    designer = models.CharField(max_length=48)
    year_released = models.IntegerField()
    min_players = models.IntegerField()
    max_players = models.IntegerField()
    recommended_age = models.IntegerField()
    estimated_time = models.DecimalField(max_digits=4, decimal_places=2)
