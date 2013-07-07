# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals
from django.contrib import messages
from django.utils.translation import ugettext_lazy

import djadmin2
from djadmin2 import renderers
from djadmin2.actions import DeleteSelectedAction

# Import your custom models
from .actions import CustomPublishAction
from .models import Post, Comment


class CommentInline(djadmin2.Admin2Inline):
    model = Comment


def unpublish_items(request, queryset):
    queryset.update(published=False)
    messages.add_message(request, messages.INFO, ugettext_lazy(u'Items unpublished'))

# Translators : action description
unpublish_items.description = ugettext_lazy('Unpublish selected items')


class PostAdmin(djadmin2.ModelAdmin2):
    list_actions = [DeleteSelectedAction, CustomPublishAction, unpublish_items]
    inlines = [CommentInline]
    search_fields = ('title', '^body')
    list_display = ('title', 'body', 'published')
    field_renderers = {
        'title': renderers.title_renderer,
    }


class CommentAdmin(djadmin2.ModelAdmin2):
    search_fields = ('body', '=post__title')
    list_filter = ['post', ]


#  Register each model with the admin
djadmin2.default.register(Post, PostAdmin)
djadmin2.default.register(Comment, CommentAdmin)

