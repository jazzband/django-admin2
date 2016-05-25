# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site
from rest_framework.relations import PrimaryKeyRelatedField

from djadmin2.apiviews import Admin2APISerializer
from djadmin2.forms import UserCreationForm, UserChangeForm
from djadmin2.site import djadmin2_site
from djadmin2.types import ModelAdmin2


class GroupSerializer(Admin2APISerializer):
    permissions = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Group


class GroupAdmin2(ModelAdmin2):
    api_serializer_class = GroupSerializer


class UserSerializer(Admin2APISerializer):
    user_permissions = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        exclude = ('password',)


class UserAdmin2(ModelAdmin2):
    create_form_class = UserCreationForm
    update_form_class = UserChangeForm
    search_fields = ('username', 'groups__name', 'first_name', 'last_name',
                     'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

    api_serializer_class = UserSerializer


#  Register each model with the admin
djadmin2_site.register(User, UserAdmin2)
djadmin2_site.register(Group, GroupAdmin2)


# Register the sites app if it's been activated in INSTALLED_APPS
if "django.contrib.sites" in settings.INSTALLED_APPS:

    class SiteAdmin2(ModelAdmin2):
        list_display = ('domain', 'name')
        search_fields = ('domain', 'name')

    djadmin2_site.register(Site, SiteAdmin2)
