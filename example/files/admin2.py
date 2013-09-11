# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import djadmin2

from .models import CaptionedFile, UncaptionedFile


djadmin2.default.register(CaptionedFile)
djadmin2.default.register(UncaptionedFile)
