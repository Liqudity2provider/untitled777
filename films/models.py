from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Film(models.Model):
    name = models.CharField(max_length=100, help_text="Film naming")
    image = models.CharField(max_length=500, )
    link = models.CharField(max_length=500, )
    rating = models.FloatField()
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-rating',)
