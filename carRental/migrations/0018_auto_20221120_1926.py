# Generated by Django 3.0.5 on 2022-11-20 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carRental', '0017_auto_20221120_1922'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='canceledorders',
            name='car',
        ),
        migrations.RemoveField(
            model_name='canceledorders',
            name='costumer',
        ),
        migrations.AddField(
            model_name='canceledorders',
            name='carId',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='canceledorders',
            name='costumerID',
            field=models.IntegerField(null=True),
        ),
    ]
