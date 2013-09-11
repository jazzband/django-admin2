# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class CaptionedFile(models.Model):
    caption = models.CharField(max_length=200, verbose_name=_('caption'))
    publication = models.FileField(upload_to='media', verbose_name=_('Uploaded File'))

    def __unicode__(self):
        return self.caption

    class Meta:
        verbose_name = _('Captioned File')
        verbose_name_plural = _('Captioned Files')


class UncaptionedFile(models.Model):
    publication = models.FileField(upload_to='media', verbose_name=_('Uploaded File'))

    def __unicode__(self):
        return unicode(self.publication)

    class Meta:
        verbose_name = _('Uncaptioned File')
        verbose_name_plural = _('Uncaptioned Files')
