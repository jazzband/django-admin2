# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

from djadmin2.site import djadmin2_site
from .models import CaptionedFile, UncaptionedFile


djadmin2_site.register(CaptionedFile)
djadmin2_site.register(UncaptionedFile)
