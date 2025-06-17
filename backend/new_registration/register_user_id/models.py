from django.db import models

class UserID(models.Model):
    user_id = models.IntegerField(unique=True) # user_ID はIntでユニークにする
    registered_at = models.DateTimeField(auto_now_add=True) # 登録日時

    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name = "User ID"
        verbose_name_plural = "User IDs"