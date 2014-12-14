# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0007_auto_20141213_2221'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('ipaddress', models.GenericIPAddressField(protocol='IPv4')),
                ('vote', models.PositiveSmallIntegerField(choices=[(0, 'Not recommend'), (1, 'Recommend')])),
                ('comment', models.ForeignKey(blank=True, to='board.Comment', related_name='_votes', null=True)),
                ('post', models.ForeignKey(blank=True, to='board.Post', related_name='_votes', null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, related_name='_votes', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='post',
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='user',
        ),
        migrations.DeleteModel(
            name='Recommendation',
        ),
    ]
