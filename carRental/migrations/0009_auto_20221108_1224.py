# Generated by Django 3.0.5 on 2022-11-08 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carRental', '0008_costumer_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='canceledOrders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customerID', models.CharField(max_length=50, null=True)),
                ('automobileId', models.CharField(max_length=10, null=True)),
                ('price', models.IntegerField(null=True)),
                ('payed', models.BooleanField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Extras',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=105)),
                ('insurance', models.IntegerField(blank=True, null=True)),
                ('fuel', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='rental',
            name='carId',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='rental',
            name='costumerID',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='rental',
            name='fullFuel',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='rental',
            name='insurance',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='rental',
            name='orderDate',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='rental',
            name='payed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='rental',
            name='finishDate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='rental',
            name='startDate',
            field=models.DateField(null=True),
        ),
    ]
