# Import your custom models
from django.contrib.auth.models import Group, User

from rest_framework.relations import PrimaryKeyRelatedField

import djadmin2
from djadmin2.forms import UserCreationForm, UserChangeForm
from djadmin2.apiviews import Admin2APISerializer

from .models import Post, Comment


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


class CommentInline(djadmin2.Admin2Inline):
    model = Comment


class PostAdmin(djadmin2.ModelAdmin2):
    inlines = [CommentInline]


class UserAdmin2(djadmin2.ModelAdmin2):
    create_form_class = UserCreationForm
    update_form_class = UserChangeForm

    api_serializer_class = UserSerializer


#  Register each model with the admin
djadmin2.default.register(Post, PostAdmin)
djadmin2.default.register(Comment)
djadmin2.default.register(User, UserAdmin2)
djadmin2.default.register(Group, GroupAdmin2)
