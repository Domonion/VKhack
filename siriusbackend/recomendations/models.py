from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)


class Subcategory(models.Model):
    name = models.CharField(max_length=256)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE)


