from django.db import models
from django.utils import timezone

class UserCredentials(models.Model):
    user_id = models.AutoField(db_column='user_ID', primary_key=True)
    '''
    Editor: Shunsuke MOROZUMI
    Date: 2025/07/03
    Description:
        user_ID カラムを自動インクリメントの主キーとして定義。
    '''
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=16)
    current_coin = models.IntegerField(blank=True, null=True)
    login_timestamp = models.DateTimeField(default=timezone.now)
    login_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
        app_label = 'register_name'


