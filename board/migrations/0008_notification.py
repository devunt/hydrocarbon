# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0007_fileattachment_imageattachment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('ipaddress', models.GenericIPAddressField(protocol='IPv4')),
                ('data', jsonfield.fields.JSONField()),
                ('from_onetime_user', models.OneToOneField(to='board.OneTimeUser', null=True, blank=True, related_name='sent_notification')),
                ('from_user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True, related_name='sent_notifications')),
                ('to_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='notifications')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
