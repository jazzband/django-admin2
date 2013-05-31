from django.conf import settings

MODEL_ADMIN_ATTRS = (
    'list_display', 'list_display_links', 'list_filter', 'admin',
    'index_view', 'detail_view', 'create_view', 'update_view', 'delete_view',
    'get_default_view_kwargs', 'get_list_actions')

ADMIN2_THEME_DIRECTORY = getattr(settings, "ADMIN2_THEME_DIRECTORY", "admin2/bootstrap")
