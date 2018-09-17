# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

from djadmin2.site import djadmin2_site
from djadmin2.types import Admin2TabularInline, ModelAdmin2
from .models import Poll, Choice


class ChoiceInline(Admin2TabularInline):
    model = Choice
    fields = '__all__'


class PollAdmin(ModelAdmin2):
    fieldsets = [
        (None, {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'


djadmin2_site.register(Poll, PollAdmin)
