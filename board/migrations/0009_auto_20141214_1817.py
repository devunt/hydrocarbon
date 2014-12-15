# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0008_auto_20141214_1355'),
    ]

    operations = [
        migrations.CreateModel(
            name='OneTimeUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('nick', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comment',
            name='onetime_user',
            field=models.OneToOneField(blank=True, to='board.OneTimeUser', null=True, related_name='comment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='onetime_user',
            field=models.OneToOneField(blank=True, to='board.OneTimeUser', null=True, related_name='post'),
            preserve_default=True,
        ),
    ]
