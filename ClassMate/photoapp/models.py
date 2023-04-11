from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from taggit.models import Tag
from django.shortcuts import get_object_or_404, redirect, render
import uuid


class Photo(models.Model):

    title = models.CharField(max_length=45)

    description = models.CharField(max_length=250)

    created = models.DateTimeField(auto_now_add=True)

    image = models.FileField(upload_to='photos/')

    thumbnail = models.ImageField(upload_to='photos/', default=image)

    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    tags = TaggableManager()

    def __str__(self):
        return self.title

    @property
    def number_of_comments(self):
        return BlogComment.objects.filter(blogpost_connected=self).count()
    
class BlogComment(models.Model):
    blogpost_connected = models.ForeignKey(Photo, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    date_posted = models.DateTimeField(auto_now_add=True)

    def str(self):
        return str(self.author) + ', ' + self.blogpost_connected.title[:40]