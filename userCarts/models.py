from django.db import models

# Create your models here.
class UserCart(models.Model):
    user_id = models.IntegerField(default=0)
    guid = models.CharField(max_length=100, default='', blank=True)
