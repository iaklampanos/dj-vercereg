# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vercereg', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavouriteWorkspaces',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('workspace', models.ForeignKey(to='vercereg.Workspace')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='favouriteworkspaces',
            unique_together=set([('user', 'workspace')]),
        ),
    ]
