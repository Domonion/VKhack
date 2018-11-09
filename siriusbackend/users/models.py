from django.db import models


class User(models.Model):
    vk_id = models.BigIntegerField(db_index=True, primary_key=True)
    banned = models.BooleanField(default=False)
    spent_time = models.FloatField(default=0.0)


class Achievement(models.Model):
    name = models.CharField(max_length=256)
    # picture


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)