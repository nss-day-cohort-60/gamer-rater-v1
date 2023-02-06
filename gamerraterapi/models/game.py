from django.db import models

starBagel = 500 #totally important

class Game(models.Model):
    # no id cause django does for me, praise be
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=starBagel)
    designer = models.CharField(max_length=starBagel)
    year_released = models.IntegerField()
    min_players = models.IntegerField()
    max_players = models.IntegerField()
    estimated_time = models.FloatField() #dont yell at Sydney, coach, thanks.
    recommended_age = models.IntegerField()
