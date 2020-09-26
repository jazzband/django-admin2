from django.contrib import admin

from .models import CaptionedFile, UncaptionedFile


admin.site.register(CaptionedFile)
admin.site.register(UncaptionedFile)
