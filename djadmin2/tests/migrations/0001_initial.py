# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BigThing',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='RendererTestModel',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('decimal', models.DecimalField(max_digits=10, decimal_places=5)),
            ],
        ),
        migrations.CreateModel(
            name='SmallThing',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='TagsTestsModel',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('field1', models.CharField(max_length=23)),
                ('field2', models.CharField(max_length=42, verbose_name='second field')),
            ],
            options={
                'verbose_name': 'Tags Test Model',
                'verbose_name_plural': 'Tags Test Models',
            },
        ),
        migrations.CreateModel(
            name='Thing',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='UtilsTestModel',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('field1', models.CharField(max_length=23)),
                ('field2', models.CharField(max_length=42, verbose_name='second field')),
            ],
            options={
                'verbose_name': 'Utils Test Model',
                'verbose_name_plural': 'Utils Test Models',
            },
        ),
    ]
