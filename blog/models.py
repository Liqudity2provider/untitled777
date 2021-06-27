from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Model of Post with next fields:
    title, content, date_posted, author
    """

    title = models.CharField(max_length=100)
    content = models.TextField()
    d = models.TextField(max_length=2, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    image = models.ImageField(blank=True, upload_to='photos')
    video = models.FileField(blank=True, upload_to='videos')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-date_posted']

