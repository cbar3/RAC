# Generated by Django 3.0.5 on 2022-11-13 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carRental', '0011_rental_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='costumer',
            field=models.CharField(max_length=70, null=True),
        ),
    ]
