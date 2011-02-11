from django.conf import settings
from django.db import models


class Image(models.Model):
    """Image model"""
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="images")
    description = models.TextField(blank=True, null=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def url(self):
        return '%s%s' % (settings.MEDIA_URL, self.image)

class Video(models.Model):
    """Video model"""
    title = models.CharField(max_length=255, blank=True, null=True)
    still = models.ImageField(upload_to="videos/stills")
    video = models.FileField(upload_to="videos")
    description = models.TextField(blank=True, null=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def url(self):
        return '%s%s' % (settings.MEDIA_URL, self.video)

