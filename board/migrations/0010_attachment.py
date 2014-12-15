# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import board.models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0009_auto_20141214_1817'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('file', models.FileField(upload_to=board.models.upload_to_func)),
                ('content_type', models.CharField(max_length=64)),
                ('checksum', models.CharField(max_length=64)),
                ('dlcount', models.PositiveIntegerField(default=0)),
                ('post', models.ForeignKey(to='board.Post', related_name='attachments')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
