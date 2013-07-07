# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

from django.conf import settings


# Restricts the attributes that are passed from ModelAdmin2 classes to their
#   views. This is a security feature.
# See the docstring on djadmin2.types.ModelAdmin2 for more detail.
MODEL_ADMIN_ATTRS = (
    'list_display', 'list_display_links', 'list_filter', 'admin',
    'search_fields',
    'field_renderers',
    'index_view', 'detail_view', 'create_view', 'update_view', 'delete_view',
    'get_default_view_kwargs', 'get_list_actions',
    'actions_on_bottom', 'actions_on_top',
    'save_on_top', 'save_on_bottom')

ADMIN2_THEME_DIRECTORY = getattr(settings, "ADMIN2_THEME_DIRECTORY", "djadmin2/bootstrap")
