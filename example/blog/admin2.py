# Import the Admin2 base class
from djadmin2.models import Admin2

# Import your custom models
from .models import Post, Comment

# Instantiate the Admin2 class
# Then attach the admin2 object to your model
Post.admin2 = Admin2()
Comment.admin2 = Admin2()
