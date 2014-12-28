# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0016_auto_20141227_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='contents',
            field=redactor.fields.RedactorField(),
            preserve_default=True,
        ),
    ]
