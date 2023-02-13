from django.db import models

class GameReview(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    player = models.ForeignKey("Player", on_delete=models.SET_NULL, null=True)
    review = models.CharField(max_length=10000)
    date_reviewed = models.DateField(auto_now=True, null=True, blank=True)
