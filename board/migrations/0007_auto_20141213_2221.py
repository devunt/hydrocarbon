# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0006_auto_20141213_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='comment',
            field=models.ForeignKey(related_name='_recommendations', null=True, to='board.Comment', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='post',
            field=models.ForeignKey(related_name='_recommendations', null=True, to='board.Post', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='user',
            field=models.ForeignKey(related_name='_recommendations', null=True, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
