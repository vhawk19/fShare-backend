# Generated by Django 4.0.4 on 2022-05-29 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='torrent_file',
        ),
        migrations.AddField(
            model_name='message',
            name='magnet_uri',
            field=models.TextField(null=True),
        ),
    ]
