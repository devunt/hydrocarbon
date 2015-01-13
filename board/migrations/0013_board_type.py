# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0012_remove_notification_ipaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Staff only'), (2, 'List type')], default=2),
            preserve_default=True,
        ),
    ]
