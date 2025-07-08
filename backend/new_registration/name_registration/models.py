from django.db import models

# Create your models here.
class UserCredentials(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=10)
    password = models.CharField(max_length=16)
    current_coin = models.IntegerField(default=0)
    login_timestamp = models.DateTimeField(auto_now_add=True)
    login_count = models.IntegerField(default=0)
    number_of_wins = models.IntegerField(default=0)
    number_of_losses = models.IntegerField(default=0)
