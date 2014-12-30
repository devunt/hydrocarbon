# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


def siteconf_func(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    db_alias = schema_editor.connection.alias
    Site.objects.using(db_alias).create(
        domain='herocomics.kr',
        name='히어로코믹스',
    )

class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('sites', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('email', models.EmailField(verbose_name='email address', unique=True, max_length=255, db_index=True)),
                ('is_staff', models.BooleanField(verbose_name='staff status', default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(verbose_name='active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('nickname', models.CharField(unique=True, max_length=16)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', verbose_name='groups', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', verbose_name='user permissions', to='auth.Permission', blank=True, help_text='Specific permissions for this user.')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(
            code=siteconf_func,
            reverse_code=None,
            atomic=False,
        ),
    ]
