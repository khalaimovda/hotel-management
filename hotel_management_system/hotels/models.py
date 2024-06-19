from django.db import models


class City(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)


class Hotel(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    city = models.ForeignKey(to=City, on_delete=models.CASCADE, related_name='hotels')

