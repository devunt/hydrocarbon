# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0005_auto_20141213_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='comment',
            field=models.ForeignKey(null=True, to='board.Comment', related_name='recommendations', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='announcement',
            name='post',
            field=models.OneToOneField(to='board.Post', related_name='announcement'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='post',
            field=models.ForeignKey(null=True, to='board.Post', related_name='recommendations', blank=True),
            preserve_default=True,
        ),
    ]
