import os
from django.conf import settings
from django.db import models
from django.urls import reverse
from dotenv import load_dotenv
from .tasks import send_email_task

load_dotenv()


class Post(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        """
        Modified to also send emails to all user,
        subscribed to post's author's blog
        """
        super().save(*args, **kwargs)
        emails = [blog.owner.email for blog in self.author.subscribers.all()]
        post_url = os.getenv('SITE_URL') + reverse('post-detail',
                                                   kwargs={'pk': self.pk})
        send_email_task.delay(self.author.username, post_url, emails)

    def __str__(self):
        return self.title


class Blog(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 related_name='owner')
    subscribed_to = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           blank=True,
                                           related_name='subscribers')
    read_posts = models.ManyToManyField(Post, blank=True,
                                        related_name='read_by')

    def __str__(self):
        return f'Owner: {self.owner.username}'
