# Generated by Django 3.0.4 on 2020-05-14 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelos', '0006_auto_20200514_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarjeta',
            name='dni_titular',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]