# Generated by Django 2.0.6 on 2018-07-15 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20180713_1634'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shift',
            old_name='time',
            new_name='A',
        ),
        migrations.AddField(
            model_name='shift',
            name='B',
            field=models.PositiveIntegerField(default=7),
        ),
        migrations.AddField(
            model_name='shift',
            name='C',
            field=models.PositiveIntegerField(default=7),
        ),
    ]