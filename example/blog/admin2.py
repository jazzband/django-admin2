
# Import your custom models
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, Permission, User


import djadmin2
from djadmin2.models import ModelAdmin2


class UserAdmin2(ModelAdmin2):
    create_form_class = UserCreationForm
    update_form_class = UserChangeForm


#  Register each model with the admin
djadmin2.default.register(Post)
djadmin2.default.register(Comment)
djadmin2.default.register(User, UserAdmin2)
djadmin2.default.register(Permission)
djadmin2.default.register(Group)
