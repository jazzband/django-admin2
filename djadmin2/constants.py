from django.conf import settings

MODEL_ADMIN_ATTRS = (
                    'list_display', 'list_display_links', 'list_filter',
                    'admin', 'has_permission', 'has_add_permission',
                    'has_edit_permission', 'has_delete_permission', 'get_actions'
                         )

ADMIN2_THEME_DIRECTORY = getattr(settings, "ADMIN2_THEME_DIRECTORY", "admin2/bootstrap")
