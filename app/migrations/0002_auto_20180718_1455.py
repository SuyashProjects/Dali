# Generated by Django 2.0.6 on 2018-07-18 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='model',
            field=models.CharField(max_length=6),
        ),
    ]
