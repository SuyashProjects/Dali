# Generated by Django 2.0.6 on 2018-06-25 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_config_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='ratio',
            field=models.IntegerField(null=True),
        ),
    ]