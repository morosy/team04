from django.db import models

class UserID(models.Model):
    # users テーブルの user_ID カラムにマッピング
    user_id = models.IntegerField(primary_key=True, db_column='user_ID') # <-- primary_key=True と db_column='user_ID'

    # init.sql の users テーブルには registered_at がないので、
    # もしこのフィールドが必要なら、users テーブルにも追加するか、別のモデルに移動
    # registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # このモデルが users テーブルを参照することを明示
        db_table = 'users'
        # このモデルは既存のテーブルを参照するだけで、Djangoのマイグレーションでは管理しない
        # つまり、Djangoがこのモデルのためにテーブルを作成したり変更したりしない
        managed = False # <-- これが重要！

    def __str__(self):
        return str(self.user_id)
