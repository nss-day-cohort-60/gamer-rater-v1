from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.CharField(max_length=1024)
    dates_available = models.CharField(max_length=50)

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
