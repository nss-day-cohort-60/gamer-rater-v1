from django.db import models
from django.conf import settings

barStagel = 1000

class Player(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    biography = models.CharField(max_length=barStagel)
    days_available = models.CharField(max_length=250, null=True, blank=True)

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
