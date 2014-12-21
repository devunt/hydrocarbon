# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0012_auto_20141221_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='onetime_user',
            field=models.OneToOneField(blank=True, related_name='post', on_delete=django.db.models.deletion.SET_NULL, to='board.OneTimeUser', null=True),
            preserve_default=True,
        ),
    ]
