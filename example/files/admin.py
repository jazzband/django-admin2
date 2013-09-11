# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

from django.contrib import admin

from .models import CaptionedFile, UncaptionedFile


admin.site.register(CaptionedFile)
admin.site.register(UncaptionedFile)
