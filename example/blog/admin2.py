from django.contrib import messages

import djadmin2
from djadmin2.actions import DeleteSelectedAction

# Import your custom models
from .actions import CustomPublishAction
from .models import Post, Comment


class CommentInline(djadmin2.Admin2Inline):
    model = Comment


def unpublish_items(request, queryset):
    queryset.update(published=False)
    messages.add_message(request, messages.INFO, u'Items unpublished')

unpublish_items.description = 'Unpublish selected items'


class PostAdmin(djadmin2.ModelAdmin2):
    list_actions = [DeleteSelectedAction, CustomPublishAction, unpublish_items]
    inlines = [CommentInline]
    search_fields = ('title', '^body')
    list_filter = ['published', ]


class CommentAdmin(djadmin2.ModelAdmin2):
    search_fields = ('body', '=post__title')
    list_filter = ['post', ]


#  Register each model with the admin
djadmin2.default.register(Post, PostAdmin)
djadmin2.default.register(Comment, CommentAdmin)
