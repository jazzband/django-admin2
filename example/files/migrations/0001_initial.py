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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('caption', models.CharField(max_length=200, verbose_name='caption')),
                ('publication', models.FileField(upload_to='media', verbose_name='Uploaded File')),
            ],
            options={
                'verbose_name': 'Captioned File',
                'verbose_name_plural': 'Captioned Files',
            },
        ),
        migrations.CreateModel(
            name='UncaptionedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('publication', models.FileField(upload_to='media', verbose_name='Uploaded File')),
            ],
            options={
                'verbose_name': 'Uncaptioned File',
                'verbose_name_plural': 'Uncaptioned Files',
            },
        ),
    ]
