from django.db import models
from django.conf import settings


class Category(models.Model):
    class TypeChoice(models.TextChoices):
        OUT = "OUT"
        IN = "IN"

    name = models.CharField(max_length=25, db_index=True, unique=True)
    type = models.CharField(max_length=3, choices=TypeChoice.choices)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Action(models.Model):

    issuer = models.CharField(max_length=60)
    amount_dollar = models.DecimalField(max_digits=11, decimal_places=2)
    amount_sum = models.DecimalField(max_digits=11, decimal_places=2)
    description = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, db_index=True)
    dolar_price = models.DecimalField(max_digits=11, decimal_places=2)
    issued = models.DateTimeField(db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
