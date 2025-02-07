from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class MyUser(AbstractUser):
    image = models.ImageField('Фото', blank=True)
    


class Achievement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_achieved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Coin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='coins')
    amount = models.IntegerField(default=0)
    date_awarded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} coins"
    
