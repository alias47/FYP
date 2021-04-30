# Generated by Django 3.1.1 on 2021-04-29 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0026_auto_20210429_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
