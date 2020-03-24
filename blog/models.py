from django.conf import settings
from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Blog(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 related_name='owner')
    subscribed_to = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           blank=True,
                                           related_name='subscribed_to')
    read_posts = models.ManyToManyField(Post, blank=True,
                                        related_name='read_posts')

    def __str__(self):
        return f'Owner: {self.owner.username}'
