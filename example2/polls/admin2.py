import djadmin2

from .models import Poll, Choice


# class ChoiceInline(admin.StackedInline):
class ChoiceInline(djadmin2.Admin2Inline):
    model = Choice
    extra = 3


class PollAdmin(djadmin2.ModelAdmin2):
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question', 'pub_date', 'was_published_recently')


djadmin2.default.register(Poll, PollAdmin)
djadmin2.default.register(Choice)
