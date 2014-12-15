# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0010_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='post',
            field=models.ForeignKey(blank=True, null=True, to='board.Post', related_name='attachments'),
            preserve_default=True,
        ),
    ]
