# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0014_auto_20141222_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='contents',
            field=redactor.fields.RedactorField(),
            preserve_default=True,
        ),
    ]
