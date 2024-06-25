from django.db import models


class City(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Hotel(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    city = models.ForeignKey(to=City, on_delete=models.CASCADE, related_name='hotels')

    class Meta:
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotels'

    def __str__(self):
        return self.name
