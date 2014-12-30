# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone
import redactor.fields
from django.conf import settings


def siteconf_func(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    db_alias = schema_editor.connection.alias
    Site.objects.using(db_alias).create(
        domain='herocomics.kr',
        name='히어로코믹스',
    )


class Migration(migrations.Migration):

    replaces = [('board', '0001_initial'), ('board', '0002_auto_20141210_2117'), ('board', '0003_attachment_checksum'), ('board', '0004_auto_20141211_1736'), ('board', '0005_auto_20141213_1307'), ('board', '0006_auto_20141213_2149'), ('board', '0007_auto_20141213_2221'), ('board', '0008_auto_20141214_1355'), ('board', '0009_auto_20141214_1817'), ('board', '0010_attachment'), ('board', '0011_auto_20141215_1514'), ('board', '0012_auto_20141221_1249'), ('board', '0013_auto_20141221_2059'), ('board', '0014_auto_20141222_1913'), ('board', '0015_auto_20141227_1704'), ('board', '0016_auto_20141227_2033'), ('board', '0017_auto_20141228_1146'), ('board', '0018_auto_20141228_2307'), ('board', '0019_auto_20141228_2318'), ('board', '0020_auto_20141229_0103'), ('board', '0021_auto_20141229_2017'), ('board', '0022_auto_20141229_2347')]

    dependencies = [
        ('sites', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nickname', models.CharField(max_length=16, unique=True)),
                ('groups', models.ManyToManyField(to='auth.Group', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', blank=True, verbose_name='groups', related_query_name='user')),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', related_name='user_set', help_text='Specific permissions for this user.', blank=True, verbose_name='user permissions', related_query_name='user')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(
            code=siteconf_func,
            reverse_code=None,
            atomic=False,
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('slug', models.SlugField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=8)),
                ('slug', models.SlugField()),
                ('board', models.ForeignKey(to='board.Board')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('ipaddress', models.GenericIPAddressField(protocol='IPv4')),
                ('contents', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(to='board.Comment', related_name='subcomments', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('ipaddress', models.GenericIPAddressField(protocol='IPv4')),
                ('title', models.CharField(max_length=32)),
                ('contents', models.TextField()),
                ('viewcount', models.PositiveIntegerField(default=0)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField()),
                ('board', models.ForeignKey(to='board.Board')),
                ('category', models.ForeignKey(to='board.Category', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='board.Tag', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='posts', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(to='board.Post', related_name='comments'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='comments', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='announcement',
            name='boards',
            field=models.ManyToManyField(to='board.Board', blank=True, null=True, related_name='announcements'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='announcement',
            name='post',
            field=models.OneToOneField(to='board.Post', related_name='announcement'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='board',
            field=models.ForeignKey(to='board.Board', related_name='categories'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='board',
            field=models.ForeignKey(to='board.Board', related_name='posts'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(to='board.Category', related_name='posts', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('ipaddress', models.GenericIPAddressField(protocol='IPv4')),
                ('vote', models.SmallIntegerField(choices=[(-1, 'Not recommend'), (1, 'Recommend')])),
                ('comment', models.ForeignKey(to='board.Comment', related_name='_votes', blank=True, null=True)),
                ('post', models.ForeignKey(to='board.Post', related_name='_votes', blank=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='_votes', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OneTimeUser',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
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
            field=models.OneToOneField(to='board.OneTimeUser', on_delete=django.db.models.deletion.SET_NULL, related_name='comment', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='onetime_user',
            field=models.OneToOneField(to='board.OneTimeUser', on_delete=django.db.models.deletion.SET_NULL, related_name='post', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='contents',
            field=redactor.fields.RedactorField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='contents',
            field=redactor.fields.RedactorField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='board.Tag', blank=True, null=True, related_name='posts'),
            preserve_default=True,
        ),
    ]
