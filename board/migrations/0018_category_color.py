# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0017_block'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='color',
            field=models.CharField(max_length=9, blank=True, null=True),
            preserve_default=True,
        ),
    ]
