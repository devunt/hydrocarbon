# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_auto_20141210_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='checksum',
            field=models.CharField(max_length=64, default=None),
            preserve_default=False,
        ),
    ]
