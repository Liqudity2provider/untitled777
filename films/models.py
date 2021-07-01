from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import redirect
from mptt.models import MPTTModel, TreeForeignKey
from requests import Response


class Genre(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Film(models.Model):
    name = models.CharField(max_length=100, help_text="Film naming", unique=True)
    description = models.TextField(max_length=1000, blank=True)
    image = models.ImageField(upload_to='photos')
    link = models.CharField(max_length=500, )
    rating = models.FloatField()
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-rating',)


class Comment(MPTTModel):
    film = models.ForeignKey(Film,
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    email = models.EmailField()
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    reason_for_deleting = models.TextField(blank=True)

    class MPTTMeta:
        order_insertion_by = ['publish']

    def __str__(self):
        return self.content

    def delete(self, *args, **kwargs):
        for children in self.get_children():
            children.delete()
        self.deleted = True
        self.save()
