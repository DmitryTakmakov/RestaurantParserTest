# Generated by Django 3.1.4 on 2020-12-29 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant_chain', models.CharField(max_length=64, unique=True, verbose_name='Название сети')),
                ('restaurant_name', models.CharField(max_length=128, verbose_name='Название ресторана')),
                ('restaurant_location_longitude', models.DecimalField(decimal_places=14, max_digits=16, verbose_name='Координаты ресторана, долгота')),
                ('restaurant_location_latitude', models.DecimalField(decimal_places=14, max_digits=16, verbose_name='Координаты ресторана, широта')),
            ],
            options={
                'verbose_name': 'Ресторан',
                'verbose_name_plural': 'Рестораны',
            },
        ),
    ]