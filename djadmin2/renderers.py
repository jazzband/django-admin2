# -*- coding: utf-8 -*-
"""
There are currently a few renderers that come directly with django-admin2. They
are used by default for some field types.
"""
from __future__ import division, absolute_import, unicode_literals

import os.path
from datetime import date, time, datetime

from django.db import models
from django.template.loader import render_to_string
from django.utils import formats, timezone
from django.utils.encoding import force_text

from djadmin2 import settings


def boolean_renderer(value, field):
    """
    Render a boolean value as icon.

    This uses the template ``renderers/boolean.html``.

    :param value: The value to process.
    :type value: boolean
    :param field: The model field instance
    :type field: django.db.models.fields.Field
    :rtype: unicode

    """
    # TODO caching of template
    tpl = os.path.join(settings.ADMIN2_THEME_DIRECTORY, 'renderers/boolean.html')
    return render_to_string(tpl, {'value': value})


def datetime_renderer(value, field):
    """
    Localize and format the specified date.

    :param value: The value to process.
    :type value: datetime.date or datetime.time or datetime.datetime
    :param field: The model field instance
    :type field: django.db.models.fields.Field
    :rtype: unicode

    """
    if isinstance(value, datetime):
        # django ticket #23466 Removing seconds from locale formats
        return formats.localize(timezone.template_localtime(value))
    elif isinstance(value, (date, time)):
        return ":".join((formats.localize(value)).split(":")[:2])
    else:
        return ":".join(value.split(":")[:2])


def title_renderer(value, field):
    """
    Render a string in title case (capitalize every word).

    :param value: The value to process.
    :type value: str or unicode
    :param field: The model field instance
    :type field: django.db.models.fields.Field
    :rtype: unicode or str

    """
    return force_text(value).title()


def number_renderer(value, field):
    """
    Format a number.

    :param value: The value to process.
    :type value: float or long
    :param field: The model field instance
    :type field: django.db.models.fields.Field
    :rtype: unicode

    """
    if isinstance(field, models.DecimalField):
        return formats.number_format(value, field.decimal_places)
    return formats.number_format(value)
