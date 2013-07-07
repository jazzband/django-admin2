# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import djadmin2

from .models import Poll, Choice


class ChoiceInline(djadmin2.Admin2Inline):
    model = Choice
    extra = 3


class PollAdmin(djadmin2.ModelAdmin2):
    fieldsets = [
        (None, {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'


djadmin2.default.register(Poll, PollAdmin)
