# Generated by Django 4.0.4 on 2022-04-22 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portholdings',
            name='numHoldings',
            field=models.DecimalField(decimal_places=20, max_digits=30),
        ),
    ]
