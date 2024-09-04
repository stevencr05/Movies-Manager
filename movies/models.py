from django.db import models
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date

class Movie(models.Model):
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=100)
    genre = models.CharField(max_length=55)
    releaseYear = models.DateField()  # Utilise DateField pour stocker les années
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

