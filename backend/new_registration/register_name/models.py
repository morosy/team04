# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone

class UserCredentials(models.Model):
    user_id = models.AutoField(db_column='user_ID', primary_key=True)  # Field name made lowercase.
    user_name = models.CharField(max_length=10)
    password = models.CharField(max_length=16)
    current_coin = models.IntegerField(blank=True, null=True)
    login_timestamp = models.DateTimeField(default=timezone.now)
    login_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
        app_label = 'register_name'


