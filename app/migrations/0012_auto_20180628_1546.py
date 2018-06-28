# Generated by Django 2.0.6 on 2018-06-28 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20180628_1040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Station10',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('time', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Station2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('time', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Station3',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('time', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Station4',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('time', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Station5',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('time', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Station6',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('time', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Station7',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('time', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Station8',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('time', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Station9',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('time', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='Station',
            new_name='Station1',
        ),
    ]
