# -*- coding: utf-8 -*-
""" Boilerplate for now, will serve a purpose soon! """
from __future__ import division, absolute_import, unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import force_text
from django.utils.encoding import python_2_unicode_compatible
from django.utils.encoding import smart_text
from django.utils.translation import ugettext, ugettext_lazy as _

from .utils import quote


class LogEntryManager(models.Manager):
    def log_action(self, user_id, obj, action_flag, change_message=''):
        content_type_id = ContentType.objects.get_for_model(obj).id
        e = self.model(None, None, user_id, content_type_id,
                       smart_text(obj.id), force_text(obj)[:200],
                       action_flag, change_message)
        e.save()


@python_2_unicode_compatible
class LogEntry(models.Model):
    ADDITION = 1
    CHANGE = 2
    DELETION = 3

    action_time = models.DateTimeField(_('action time'), auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='log_entries')
    content_type = models.ForeignKey(ContentType, blank=True, null=True,
                                     related_name='log_entries')
    object_id = models.TextField(_('object id'), blank=True, null=True)
    object_repr = models.CharField(_('object repr'), max_length=200)
    action_flag = models.PositiveSmallIntegerField(_('action flag'))
    change_message = models.TextField(_('change message'), blank=True)

    objects = LogEntryManager()

    class Meta:
        verbose_name = _('log entry')
        verbose_name_plural = _('log entries')
        ordering = ('-action_time',)

    def __repr__(self):
        return smart_text(self.action_time)

    def __str__(self):
        if self.action_flag == self.ADDITION:
            return ugettext('Added "%(object)s".') % {
                'object': self.object_repr}
        elif self.action_flag == self.CHANGE:
            return ugettext('Changed "%(object)s" - %(changes)s') % {
                'object': self.object_repr,
                'changes': self.change_message,
            }
        elif self.action_flag == self.DELETION:
            return ugettext('Deleted "%(object)s."') % {
                'object': self.object_repr}

        return ugettext('LogEntry Object')

    def is_addition(self):
        return self.action_flag == self.ADDITION

    def is_change(self):
        return self.action_flag == self.CHANGE

    def is_deletion(self):
        return self.action_flag == self.DELETION

    @property
    def action_type(self):
        if self.is_addition():
            return _('added')
        if self.is_change():
            return _('changed')
        if self.is_deletion():
            return _('deleted')
        return ''

    def get_edited_object(self):
        "Returns the edited object represented by this log entry"
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    def get_admin_url(self):
        """
        Returns the admin URL to edit the object represented by this log entry.
        This is relative to the Django admin index page.
        """
        if self.content_type and self.object_id:
            return '{0.app_label}/{0.model}/{1}'.format(
                self.content_type,
                quote(self.object_id)
            )
        return None
