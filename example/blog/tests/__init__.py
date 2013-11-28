# make sure that everything is setup for tests. Django 1.6 doesn't necessarily
# load the urls.py before the tests are run.
import example.urls

from test_apiviews import *
from test_builtin_api_resources import *
from test_permissions import *
from test_modelforms import *
from test_views import *
from test_nestedobjects import *
from test_filters import *
