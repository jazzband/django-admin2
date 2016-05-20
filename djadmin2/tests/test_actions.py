from django.test import TestCase

from ..core import Admin2
from ..actions import get_description
from .models import Thing


class TestAction(object):
    description = "Test Action Class"


def test_function():
    pass


class ActionTest(TestCase):
    def setUp(self):
        self.admin2 = Admin2()

    def test_action_description(self):
        self.admin2.register(Thing)
        self.admin2.registry[Thing].list_actions.extend([
            TestAction,
            test_function,
        ])
        self.assertEquals(
            get_description(
                self.admin2.registry[Thing].list_actions[0]
            ),
            'Delete selected items'
        )
        self.assertEquals(
            get_description(
                self.admin2.registry[Thing].list_actions[1]
            ),
            'Test Action Class'
        )
        self.assertEquals(
            get_description(
                self.admin2.registry[Thing].list_actions[2]
            ),
            'Test function'
        )
        self.admin2.registry[Thing].list_actions.remove(TestAction)
        self.admin2.registry[Thing].list_actions.remove(test_function)
