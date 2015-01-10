# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0005_auto_20150109_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='contents',
            field=froala_editor.fields.FroalaField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='contents',
            field=froala_editor.fields.FroalaField(),
            preserve_default=True,
        ),
    ]
