# Generated by Django 4.1.6 on 2023-04-10 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photoapp', '0008_alter_comment_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='slug',
            field=models.SlugField(default='nothing', max_length=200, unique=True),
        ),
    ]
