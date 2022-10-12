# Generated by Django 2.2.2 on 2022-10-07 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RentalCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(blank=True, default='', max_length=100)),
                ('companyAddress', models.CharField(blank=True, default='', max_length=100)),
                ('companyPhoneNumber', models.TextField()),
            ],
        ),
    ]
