# Generated by Django 2.2.5 on 2020-01-22 02:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_priority'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todoitem',
            name='priority',
        ),
    ]
