# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('action_time', models.DateTimeField(verbose_name='action time', auto_now=True)),
                ('object_id', models.TextField(blank=True, verbose_name='object id', null=True)),
                ('object_repr', models.CharField(max_length=200, verbose_name='object repr')),
                ('action_flag', models.PositiveSmallIntegerField(verbose_name='action flag')),
                ('change_message', models.TextField(verbose_name='change message', blank=True)),
                ('content_type', models.ForeignKey(related_name='log_entries', to='contenttypes.ContentType', blank=True, null=True)),
                ('user', models.ForeignKey(related_name='log_entries', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-action_time',),
                'verbose_name': 'log entry',
                'verbose_name_plural': 'log entries',
            },
        ),
    ]
