# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_squashed_0022_auto_20141229_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(max_length=16, unique=True, validators=[django.core.validators.MinLengthValidator(2)]),
            preserve_default=True,
        ),
    ]
