# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0020_auto_20141229_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='boards',
            field=models.ManyToManyField(to='board.Board', null=True, related_name='announcements', blank=True),
            preserve_default=True,
        ),
    ]
