# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('action_time', models.DateTimeField(verbose_name='action time', auto_now=True)),
                ('object_id', models.TextField(verbose_name='object id', null=True, blank=True)),
                ('object_repr', models.CharField(max_length=200, verbose_name='object repr')),
                ('action_flag', models.PositiveSmallIntegerField(verbose_name='action flag')),
                ('change_message', models.TextField(verbose_name='change message', blank=True)),
                ('content_type', models.ForeignKey(related_name='log_entries', null=True, blank=True, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(related_name='log_entries', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'log entry',
                'ordering': ('-action_time',),
                'verbose_name_plural': 'log entries',
            },
        ),
    ]
