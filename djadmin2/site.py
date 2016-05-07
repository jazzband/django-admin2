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