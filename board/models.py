from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    nick = models.CharField(max_length=16)

    def __str__(self):
        return str(self.user)
