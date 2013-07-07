# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

from django.db import models
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    body = models.TextField(verbose_name=_('body'))
    published = models.BooleanField(default=False, verbose_name=_('published'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')


class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name=_('post'))
    body = models.TextField(verbose_name=_('body'))

    def __unicode__(self):
        return self.body

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


#### Models needed for testing NestedObjects

@python_2_unicode_compatible
class Count(models.Model):
    num = models.PositiveSmallIntegerField()
    parent = models.ForeignKey('self', null=True)

    def __str__(self):
        return six.text_type(self.num)


class Event(models.Model):
    date = models.DateTimeField(auto_now_add=True)


class Location(models.Model):
    event = models.OneToOneField(Event, verbose_name='awesome event')


class Guest(models.Model):
    event = models.OneToOneField(Event)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "awesome guest"


class EventGuide(models.Model):
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
