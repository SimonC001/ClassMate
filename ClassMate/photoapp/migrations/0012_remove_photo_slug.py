# Generated by Django 4.1.6 on 2023-04-10 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoapp', '0011_alter_photo_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='slug',
        ),
    ]
