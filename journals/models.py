from django.db import models
import os


class Publisher(models.Model):
    name = models.CharField(max_length=256)
    logo = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Journal(models.Model):
    # Main fields
    name = models.CharField(max_length=256)
    logo = models.ImageField(upload_to='images/', blank=True, null=True)
    subscription_fee = models.DecimalField(max_digits=10, decimal_places=2)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    # Additional information
    short_description = models.TextField(blank=True)
    full_description = models.TextField(blank=True)

    def __str__(self):
        return self.name

