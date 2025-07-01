from django.db import models
from django.utils import timezone

class UserCredentials(models.Model):
    user_id = models.AutoField(db_column='user_ID', primary_key=True) 
    password = models.CharField(max_length=16)
    current_coin = models.IntegerField(blank=True, null=True)
    login_timestamp = models.DateTimeField(default=timezone.now)
    login_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
        app_label = 'register_name'


