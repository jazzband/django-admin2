from os import join

from django.conf import settings
from django.views.generic import ListView

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from .utils import get_admin2s

ADMIN2_THEME_DIRECTORY = settings.get("ADMIN2_THEME_DIRECTORY", "admin2/bootstrap")


class IndexView(LoginRequiredMixin, StaffuserRequiredMixin, ListView):

    def get_template_name(self):
        return join(ADMIN2_THEME_DIRECTORY, "index.html")

    def get_queryset(self):
        return get_admin2s()
