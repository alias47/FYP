# Generated by Django 3.1.1 on 2021-04-29 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0020_auto_20210429_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='image.category'),
        ),
    ]
