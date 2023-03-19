from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from taggit.models import Tag
from django.shortcuts import get_object_or_404, redirect, render


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
