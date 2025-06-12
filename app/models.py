from django.db import models
from enum import Enum


class Item(models.Model):
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.title


class CategoryType(Enum):
    POSITIVE = 'Positive'
    NEGATIVE = 'Negative'


class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=15,
                            choices=[(type.name, type.value) for type in CategoryType],
                            default=CategoryType.POSITIVE)
    items = models.ManyToManyField(Item, auto_created=True)

    def __str__(self):
        return self.name
