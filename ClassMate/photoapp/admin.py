from django.contrib import admin
from .models import Photo, Comment  # We import the photo model

# Register your models here.
admin.site.register(Photo)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
