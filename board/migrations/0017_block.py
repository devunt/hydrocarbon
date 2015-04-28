# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0016_auto_20150227_0159'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('ipaddress', models.GenericIPAddressField(unique=True, protocol='IPv4')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('expiration_time', models.DateTimeField()),
                ('reason', models.CharField(max_length=256)),
                ('executor', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='blocks_executed')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
