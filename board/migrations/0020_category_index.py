# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0019_auto_20150511_0158'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='index',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
