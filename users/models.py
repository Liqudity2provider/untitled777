from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.TextField(
        default='https://firebasestorage.googleapis.com/v0/b/memories-9ec47.appspot.com/o/Screenshot_4.png?alt=media&token=4a144de4-5c27-49f1-9bb0-25bc4fb19815')

    def __str__(self):
        return f'{self.user.username} Profile'
