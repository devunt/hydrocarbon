# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_auto_20141211_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='boards',
            field=models.ManyToManyField(related_name='announcements', to='board.Board'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='announcement',
            name='post',
            field=models.ForeignKey(related_name='announcements', to='board.Post'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='board',
            field=models.ForeignKey(related_name='categories', to='board.Board'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(related_name='comments', to='board.Post'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, related_name='comments'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='board',
            field=models.ForeignKey(related_name='posts', to='board.Board'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(null=True, blank=True, to='board.Category', related_name='posts'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, related_name='posts'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='post',
            field=models.ForeignKey(related_name='recommendations', to='board.Post'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='user',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, related_name='recommendations'),
            preserve_default=True,
        ),
    ]
