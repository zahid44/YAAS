# Generated by Django 2.1.2 on 2018-10-19 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0013_auto_20181019_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='is_actice',
            field=models.BooleanField(default=True),
        ),
    ]
