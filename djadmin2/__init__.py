__version__ = '0.1.1'

__author__ = 'Daniel Greenfeld'

VERSION = __version__  # synonym

# Default datetime input and output formats
ISO_8601 = 'iso-8601'

from . import core 


default = core.Admin2()
