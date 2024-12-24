from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
  
class Director(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
  
class Star(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
  
class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateField(null=True, blank=True)
    run_time = models.IntegerField(null=True, blank=True)
    genre = models.ManyToManyField(Genre, related_name='movies')
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)
    director = models.ManyToManyField(Director, related_name='movies')
    stars = models.ManyToManyField(Star, related_name='movies')

    def __str__(self):
        return self.title