# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_attachment_checksum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='post',
        ),
        migrations.DeleteModel(
            name='Attachment',
        ),
    ]
