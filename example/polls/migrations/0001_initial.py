# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200, verbose_name='choice text')),
                ('votes', models.IntegerField(default=0, verbose_name='votes')),
            ],
            options={
                'verbose_name_plural': 'choices',
                'verbose_name': 'choice',
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('question', models.CharField(max_length=200, verbose_name='question')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
            options={
                'verbose_name_plural': 'polls',
                'verbose_name': 'poll',
            },
        ),
        migrations.AddField(
            model_name='choice',
            name='poll',
            field=models.ForeignKey(to='polls.Poll', verbose_name='poll'),
        ),
    ]
