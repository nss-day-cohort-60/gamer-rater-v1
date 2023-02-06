from django.db import models

barStagel = 1000

class Player(models.Model):
    biography = models.CharField(max_length=barStagel)
    days_available = models.CharField(max_length=250)
    #? How would days available be formatted on the client  What would the entry look like?
