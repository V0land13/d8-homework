# Generated by Django 2.2.5 on 2020-01-22 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_category_todos_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=256)),
                ('priority_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Приоритет',
                'verbose_name_plural': 'Приоритеты',
            },
        ),
    ]
