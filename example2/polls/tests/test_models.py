from django.test import TestCase
from django.utils import timezone

from polls.models import Poll
from polls.models import Choice


class PollTestCase(TestCase):

    def setUp(self):
        self.poll = Poll.objects.create(
            question="mine",
            pub_date=timezone.now()
        )
        self.poll.save()

    def test_creation(self):
        p = Poll.objects.create(
            question="lo lo",
            pub_date=timezone.now()
        )
        p.save()
        self.assertEqual(Poll.objects.count(), 2)
        # Cause setup created one already

    def test_update(self):
        # TODO Add code
        # change self.poll.question to "yours"
        self.poll.question = "yours"
        # do self.poll.save()
        self.poll.save()

        # TODO Add assertions
        # make p = Poll.objects.get()
        p = Poll.objects.get()
        # add self.assertEqual(p.question, "yours")
        self.assertEqual(p.question, "yours")

    def test_delete(self):
        # TODO Add code
        # get from the db using poll question
        p = Poll.objects.get()
        # delete poll from the db
        p.delete()

        # TODO Add assertions
        # check if d is empty
        self.assertEqual(Poll.objects.count(), 0)


class ChoiceTestCase(TestCase):

    def setUp(self):
        self.poll = Poll.objects.create(
            question="mine",
            pub_date=timezone.now()
        )
        self.poll.save()
        self.choice = Choice.objects.create(
            poll=self.poll,
            choice_text="first text",
            votes=2
        )

    def test_choice_creation(self):
        # code
        # add another choice
        p = Choice.objects.create(
            poll=self.poll,
            choice_text="second text",
            votes=5
        )
        p.save()

        # assertion
        #check that there are two choices
        self.assertEqual(Choice.objects.count(), 2)

    def test_choice_update(self):
        # code
        # change a choice
        self.choice.choice_text = "third text"
        self.choice.save()
        p = Choice.objects.get()

        # assertion
        # check the choice is egal to the new choice
        self.assertEqual(p.choice_text, "third text")

    def test_choice_delete(self):
        # code
        # get Choice obj and delete it
        p = Choice.objects.get()
        p.delete()

        # assertion
        # check there are nothing in db
        self.assertEqual(Choice.objects.count(), 0)
