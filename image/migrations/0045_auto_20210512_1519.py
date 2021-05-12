# Generated by Django 3.0.6 on 2021-05-12 09:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0044_auto_20210512_0316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myrating',
            name='rating',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
    ]
