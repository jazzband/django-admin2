# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

from .models import CaptionedFile, UncaptionedFile
from djadmin2 import site

site.default.register(CaptionedFile)
site.default.register(UncaptionedFile)
