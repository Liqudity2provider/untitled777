from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    """
    Model of Post with next fields:
    title, content, date_posted, author
    """

    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.CharField(max_length=30, blank=True)
    image = models.TextField(blank=True)
    video = models.TextField(blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-date_posted']


class TempVideo(models.Model):
    video_name = models.CharField(max_length=200)
    videofile = models.FileField(upload_to='blog/temp_videos/')
