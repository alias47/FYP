# Generated by Django 3.1.1 on 2021-04-29 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0025_auto_20210429_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='image.category'),
        ),
    ]
