# backend/keiba_auth/login_request/models.py

from django.db import models
from django.utils import timezone

from new_registration.register_name.models import UserCredentials as SystemUser

class LoginAttemptHistory(models.Model):
    # UserCredentials モデル (usersテーブルにマッピングされているもの) への外部キー
    # db_columnとto_fieldで、既存のusersテーブルのuser_IDカラムと連携させます。
    user = models.ForeignKey(SystemUser, on_delete=models.CASCADE, db_column='user_ID', to_field='user_id')
    attempt_timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    class Meta:
        db_table = 'login_attempt_history' # Djangoが管理する新しいテーブル
        # managed = True (デフォルトなので省略可能)

        '''
        editor: Shunsuke MOROZUMI
        Date: 2025/07/03
        Usage: Djangoが管理するテーブルではなく、手動で管理するテーブルにするためにmanagedをFalseに設定
        Note:
            - docker-compose.ymlのvolumesでマウントされているデータベースファイルを使用するため、
              Djangoのマイグレーションによる自動生成を防ぐためにmanagedをFalseに設定
        '''
        managed = False

    def __str__(self):
        return f"Attempt by {self.user.user_name} at {self.attempt_timestamp} - Success: {self.success}"