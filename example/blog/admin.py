from django.contrib import admin

from .models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline, ]
    search_fields = ('title', 'body')
    list_filter = ['published', 'title' ]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
