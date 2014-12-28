# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0018_auto_20141228_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='nick',
            field=models.CharField(max_length=16, unique=True),
            preserve_default=True,
        ),
    ]
