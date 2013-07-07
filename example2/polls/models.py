# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Poll(models.Model):
    question = models.CharField(max_length=200, verbose_name=_('question'))
    pub_date = models.DateTimeField(verbose_name=_('date published'))

    def __unicode__(self):
        return self.question

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = _('Published recently?')

    class Meta:
        verbose_name = _('poll')
        verbose_name_plural = _('polls')


class Choice(models.Model):
    poll = models.ForeignKey(Poll, verbose_name=_('poll'))
    choice_text = models.CharField(max_length=200, verbose_name=_('choice text'))
    votes = models.IntegerField(default=0, verbose_name=_('votes'))

    def __unicode__(self):
        return self.choice_text

    class Meta:
        verbose_name = _('choice')
        verbose_name_plural = _('choices')
