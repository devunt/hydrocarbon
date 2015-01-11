# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0009_auto_20150111_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='checked_time',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
