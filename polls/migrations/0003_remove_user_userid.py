# Generated by Django 3.2.dev20200814111336 on 2020-08-22 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_session_user_vote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='userID',
        ),
    ]