from django.db import models

# Create your models here.

# backend/register_name/models.py
from django.db import models
from new_registration.register_user_id.models import UserID # 以前作ったUserIDモデルをインポート

class UserCredentials(models.Model):
    # ユーザーIDはUserIDモデルへの外部キーとして関連付ける
    user_id = models.OneToOneField(UserID, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255) # パスワードはハッシュ化して保存すべきですが、ここではシンプルにCharField

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User Credential"
        verbose_name_plural = "User Credentials"
