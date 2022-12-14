# Generated by Django 3.0.5 on 2022-11-20 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carRental', '0016_auto_20221117_2045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='canceledorders',
            name='automobileId',
        ),
        migrations.RemoveField(
            model_name='canceledorders',
            name='customerID',
        ),
        migrations.AddField(
            model_name='canceledorders',
            name='car',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='carRental.Car'),
        ),
        migrations.AddField(
            model_name='canceledorders',
            name='costumer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='carRental.Costumer'),
        ),
    ]
