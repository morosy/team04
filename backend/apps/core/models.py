from django.db import models

class Horse(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10)
    trainer = models.CharField(max_length=100)

    def __str__(self):
        return self.name

from django.db import models

class User(models.Model):
    user_name = models.CharField(max_length=10)
    password = models.CharField(max_length=16)
    current_coin = models.IntegerField(default=0)
    login_timestamp = models.DateTimeField(auto_now_add=True)
    login_count = models.IntegerField(default=0)
    number_of_wins = models.IntegerField(default=0)
    number_of_losses = models.IntegerField(default=0)

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    request_timestamp = models.DateTimeField(auto_now_add=True)
