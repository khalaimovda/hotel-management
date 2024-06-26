import uuid

from django.db import models


class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Hotel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    city = models.ForeignKey(to=City, on_delete=models.CASCADE, related_name='hotels')

    class Meta:
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotels'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name
