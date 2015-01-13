# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0011_auto_20150111_1842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='ipaddress',
        ),
    ]
