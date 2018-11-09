from django.db import models

import users.models as users
import events.models as events

class Category(models.Model):
    name = models.CharField(max_length=256)


class Subcategory(models.Model):
    name = models.CharField(max_length=256)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE)


class UserInterests(models.Model):
    user = models.ForeignKey(users.User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True)


class EventCategories(models.Model):
    event = models.ForeignKey(events.Event, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class EventSubcategories(models.Model):
    event = models.ForeignKey(events.Event, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Category, on_delete=models.CASCADE)

