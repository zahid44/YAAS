# Generated by Django 2.1.2 on 2018-10-23 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0019_auto_20181021_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to='auction.Profile'),
        ),
    ]
