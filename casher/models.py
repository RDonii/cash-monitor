from django.db import models
from django.conf import settings


class Category(models.Model):
    class TypeChoice(models.TextChoices):
        OUT = "OUT"
        IN = "IN"

    name = models.CharField(max_length=25, db_index=True, unique=True)
    type = models.CharField(max_length=3, choices=TypeChoice.choices)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Income(models.Model):
    class CurrencyChoice(models.TextChoices):
        USD = "USD"
        UZS = "UZS"

    person = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CurrencyChoice.choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Outcome(models.Model):
    class CurrencyChoice(models.TextChoices):
        USD = "USD"
        UZS = "UZS"

    person = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CurrencyChoice.choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
