# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0011_auto_20141215_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='vote',
            field=models.SmallIntegerField(choices=[(-1, 'Not recommend'), (1, 'Recommend')]),
            preserve_default=True,
        ),
    ]
