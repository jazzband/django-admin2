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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('choice_text', models.CharField(max_length=200, verbose_name='choice text')),
                ('votes', models.IntegerField(verbose_name='votes', default=0)),
            ],
            options={
                'verbose_name': 'choice',
                'verbose_name_plural': 'choices',
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=200, verbose_name='question')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
            options={
                'verbose_name': 'poll',
                'verbose_name_plural': 'polls',
            },
        ),
        migrations.AddField(
            model_name='choice',
            name='poll',
            field=models.ForeignKey(
                verbose_name='poll',
                to='polls.Poll',
                on_delete=models.CASCADE),
        ),
    ]
