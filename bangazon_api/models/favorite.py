from django.db import models
from django.contrib.auth.models import User


class Favorite(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites')
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
