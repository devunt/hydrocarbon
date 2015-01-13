# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0013_board_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='type',
            field=models.PositiveSmallIntegerField(default=2, choices=[(1, 'Announcement board'), (2, 'List type')]),
            preserve_default=True,
        ),
    ]
