# Generated by Django 2.2.16 on 2023-02-14 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0016_post_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='created',
        ),
    ]