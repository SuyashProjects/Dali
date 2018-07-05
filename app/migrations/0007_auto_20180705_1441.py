# Generated by Django 2.0.6 on 2018-07-05 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20180705_1306'),
    ]

    operations = [
        migrations.RenameField(
            model_name='station',
            old_name='time',
            new_name='stn1',
        ),
        migrations.RemoveField(
            model_name='config',
            name='Station',
        ),
        migrations.AddField(
            model_name='station',
            name='SKU',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.Config'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='station',
            name='stn10',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='station',
            name='stn2',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='station',
            name='stn3',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='station',
            name='stn4',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='station',
            name='stn5',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='station',
            name='stn6',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='station',
            name='stn7',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='station',
            name='stn8',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='station',
            name='stn9',
            field=models.PositiveIntegerField(null=True),
        ),
    ]