# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0013_auto_20141221_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='onetime_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.SET_NULL, to='board.OneTimeUser', null=True, blank=True, related_name='comment'),
            preserve_default=True,
        ),
    ]
