from django.db import models
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date
from PIL import Image  # Pour redimensionner l'image

class Movie(models.Model):
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=100)
    genre = models.CharField(max_length=55)
    releaseYear = models.DateField()  # Utilise DateField pour stocker les années
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(null=True, default=0)
    duration = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    production_company = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=255, null=True, blank=True)
    
    # Nouveau champ pour stocker l'image
    image = models.ImageField(upload_to='movies_images/', null=True, blank=True)

    def __str__(self):
        return self.title

    # Méthode pour redimensionner l'image
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            # Redimensionner l'image à 340x510
            if img.height > 510 or img.width > 340:
                output_size = (340, 510)
                img = img.resize(output_size)
                img.save(self.image.path)
