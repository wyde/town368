# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-24 12:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('rid', models.AutoField(primary_key=True, serialize=False)),
                ('station_sid', models.IntegerField(blank=True, null=True)),
                ('update_t', models.DateTimeField(blank=True, null=True)),
                ('record_t', models.DateTimeField(blank=True, null=True)),
                ('weekday', models.CharField(blank=True, max_length=3, null=True)),
                ('wx', models.CharField(blank=True, max_length=32, null=True)),
                ('t', models.IntegerField(blank=True, null=True)),
                ('at', models.IntegerField(blank=True, null=True)),
                ('beaufort', models.CharField(blank=True, max_length=16, null=True)),
                ('wind_dir', models.CharField(blank=True, max_length=3, null=True)),
                ('rh', models.CharField(blank=True, max_length=4, null=True)),
                ('pop', models.CharField(blank=True, max_length=4, null=True)),
                ('ci', models.CharField(blank=True, max_length=8, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'report',
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('sid', models.IntegerField(primary_key=True, serialize=False)),
                ('district', models.CharField(blank=True, max_length=8, null=True, unique=True)),
            ],
            options={
                'managed': False,
                'db_table': 'station',
            },
        ),
    ]
