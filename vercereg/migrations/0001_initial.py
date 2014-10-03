# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.CharField(max_length=3, choices=[(b'IN', b'In'), (b'OUT', b'Out')])),
                ('name', models.CharField(max_length=30)),
                ('s_type', models.CharField(max_length=30, null=True, blank=True)),
                ('d_type', models.CharField(max_length=30, null=True, blank=True)),
                ('comment', models.CharField(max_length=200, null=True, blank=True)),
                ('is_array', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FunctionParameters',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('param_name', models.CharField(max_length=30)),
                ('param_type', models.CharField(default=None, max_length=30, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GenericDef',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pckg', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('gendef_description', models.CharField(max_length=200)),
                ('creation_date', models.DateTimeField()),
                ('group', models.ForeignKey(to='auth.Group')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GenericSig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pckg', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('gensig_description', models.CharField(max_length=200)),
                ('creation_date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FunctionSig',
            fields=[
                ('genericsig_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='vercereg.GenericSig')),
                ('return_type', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
            bases=('vercereg.genericsig',),
        ),
        migrations.CreateModel(
            name='Implementation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pckg', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('code', models.TextField(blank=True)),
                ('group', models.ForeignKey(to='auth.Group')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LiteralSig',
            fields=[
                ('genericsig_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='vercereg.GenericSig')),
                ('value', models.CharField(max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('vercereg.genericsig',),
        ),
        migrations.CreateModel(
            name='Modifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=30)),
                ('connection', models.ForeignKey(to='vercereg.Connection')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PESig',
            fields=[
                ('genericsig_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='vercereg.GenericSig')),
                ('kind', models.CharField(max_length=10, choices=[(b'ABSTRACT', b'Abstract'), (b'PRIMITIVE', b'Primitive'), (b'COMPOSITE', b'Composite')])),
            ],
            options={
                'abstract': False,
            },
            bases=('vercereg.genericsig',),
        ),
        migrations.CreateModel(
            name='WorkflowSig',
            fields=[
                ('genericsig_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='vercereg.GenericSig')),
            ],
            options={
                'abstract': False,
            },
            bases=('vercereg.genericsig',),
        ),
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('group', models.ForeignKey(to='auth.Group')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='implementation',
            name='parent_sig',
            field=models.ForeignKey(to='vercereg.GenericSig'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='implementation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='implementation',
            name='workspace',
            field=models.ForeignKey(to='vercereg.Workspace'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericsig',
            name='gendef',
            field=models.ForeignKey(to='vercereg.GenericDef'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericsig',
            name='group',
            field=models.ForeignKey(to='auth.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericsig',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericsig',
            name='workspace',
            field=models.ForeignKey(to='vercereg.Workspace'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericdef',
            name='workspace',
            field=models.ForeignKey(to='vercereg.Workspace'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='functionparameters',
            name='parent_function',
            field=models.ForeignKey(to='vercereg.FunctionSig'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='connection',
            name='pesig',
            field=models.ForeignKey(to='vercereg.PESig'),
            preserve_default=True,
        ),
    ]
