# Generated by Django 2.1.2 on 2018-10-18 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0009_bid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auction',
            options={'ordering': ['-created']},
        ),
        migrations.AlterField(
            model_name='auction',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
