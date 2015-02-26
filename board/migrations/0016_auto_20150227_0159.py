# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0015_auto_20150113_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileattachment',
            name='name',
            field=models.CharField(max_length=250),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imageattachment',
            name='name',
            field=models.CharField(max_length=250),
            preserve_default=True,
        ),
    ]
