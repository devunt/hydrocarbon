# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0020_category_index'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['index', 'color']},
        ),
    ]
