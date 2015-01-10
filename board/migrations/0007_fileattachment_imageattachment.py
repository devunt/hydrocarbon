# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import board.utils


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0006_auto_20150109_2254'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('file', models.FileField(max_length=256, upload_to=board.utils.get_upload_path)),
                ('checksum', models.CharField(max_length=32, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImageAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('file', models.ImageField(max_length=256, upload_to=board.utils.get_upload_path)),
                ('checksum', models.CharField(max_length=32, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
