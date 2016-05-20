# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CaptionedFile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('caption', models.CharField(max_length=200, verbose_name='caption')),
                ('publication', models.FileField(verbose_name='Uploaded File', upload_to='captioned-files')),
            ],
            options={
                'verbose_name': 'Captioned File',
                'verbose_name_plural': 'Captioned Files',
            },
        ),
        migrations.CreateModel(
            name='UncaptionedFile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('publication', models.FileField(verbose_name='Uploaded File', upload_to='uncaptioned-files')),
            ],
            options={
                'verbose_name': 'Uncaptioned File',
                'verbose_name_plural': 'Uncaptioned Files',
            },
        ),
    ]
