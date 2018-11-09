from django.db import models


class User(models.Model):
    vk_id = models.BigIntegerField(db_index=True, primary_key=True)
    banned = models.BooleanField(default=False)
    spent_time = models.FloatField(default=0.0)
