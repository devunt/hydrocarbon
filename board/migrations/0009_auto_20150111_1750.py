# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0008_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 1, 0, 00, 0, 000000, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vote',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 1, 0, 00, 00, 000000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
