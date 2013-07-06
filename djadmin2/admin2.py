from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site


from rest_framework.relations import PrimaryKeyRelatedField

import djadmin2
from djadmin2.forms import UserCreationForm, UserChangeForm
from djadmin2.apiviews import Admin2APISerializer


class GroupSerializer(Admin2APISerializer):
    permissions = PrimaryKeyRelatedField(many=True)

    class Meta:
        model = Group


class GroupAdmin2(djadmin2.ModelAdmin2):
    api_serializer_class = GroupSerializer


class UserSerializer(Admin2APISerializer):
    user_permissions = PrimaryKeyRelatedField(many=True)

    class Meta:
        model = User
        exclude = ('passwords',)


class UserAdmin2(djadmin2.ModelAdmin2):
    create_form_class = UserCreationForm
    update_form_class = UserChangeForm
    search_fields = ('username', 'groups__name')

    api_serializer_class = UserSerializer


class SiteAdmin2(djadmin2.ModelAdmin2):
    list_display = ('domain', 'name')
    search_fields = ('domain', 'name')


#  Register each model with the admin
djadmin2.default.register(User, UserAdmin2)
djadmin2.default.register(Group, GroupAdmin2)
djadmin2.default.register(Site, SiteAdmin2)
