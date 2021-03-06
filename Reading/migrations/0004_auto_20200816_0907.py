# Generated by Django 3.0.8 on 2020-08-16 09:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reading', '0003_profile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='pages',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='read',
            name='target',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='read',
            name='progress',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
