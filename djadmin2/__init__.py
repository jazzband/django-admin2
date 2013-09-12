# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

__version__ = '0.6.0rc1'

__author__ = 'Daniel Greenfeld & Contributors'

VERSION = __version__  # synonym

# Default datetime input and output formats
ISO_8601 = 'iso-8601'

from . import core
from . import types


default = core.Admin2()
ModelAdmin2 = types.ModelAdmin2
Admin2TabularInline = types.Admin2TabularInline
Admin2StackedInline = types.Admin2StackedInline

# Utility to make migration between versions easier
sites = default
ModelAdmin = ModelAdmin2
AdminInline = Admin2TabularInline
Admin2Inline = Admin2TabularInline
