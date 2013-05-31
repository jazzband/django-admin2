__version__ = '0.3.0'

__author__ = 'Daniel Greenfeld & Contributors'

VERSION = __version__  # synonym

# Default datetime input and output formats
ISO_8601 = 'iso-8601'

from . import core
from . import types


default = core.Admin2()
ModelAdmin2 = types.ModelAdmin2
Admin2Inline = types.Admin2Inline
