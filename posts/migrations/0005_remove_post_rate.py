# Generated by Django 3.2.9 on 2021-11-16 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='rate',
        ),
    ]
