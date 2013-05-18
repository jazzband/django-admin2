
# Import your custom models
from .models import Post, Comment
from django.contrib.auth.models import User

import djadmin2

#  Register each model with the admin
djadmin2.default.register(Post)
djadmin2.default.register(Comment)
djadmin2.default.register(User)