# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import datetime as dt
from decimal import Decimal

from django.test import TestCase
from django.utils import six
from django.utils.translation import activate

from .. import renderers
from .models import RendererTestModel


class BooleanRendererTest(TestCase):

    def setUp(self):
        self.renderer = renderers.boolean_renderer

    def test_boolean(self):
        out1 = self.renderer(True, None)
        self.assertIn('fa fa-check', out1)
        out2 = self.renderer(False, None)
        self.assertIn('fa fa-minus', out2)

    def test_string(self):
        out1 = self.renderer('yeah', None)
        self.assertIn('fa fa-check', out1)
        out2 = self.renderer('', None)
        self.assertIn('fa fa-minus', out2)


class DatetimeRendererTest(TestCase):

    def setUp(self):
        self.renderer = renderers.datetime_renderer

    def tearDown(self):
        activate('en_US')

    def test_date_german(self):
        activate('de')
        out = self.renderer(dt.date(2013, 7, 6), None)
        self.assertEqual('6. Juli 2013', out)

    def test_date_spanish(self):
        activate('es')
        out = self.renderer(dt.date(2013, 7, 6), None)
        self.assertEqual('6 de Julio de 2013', out)

    def test_date_default(self):
        out = self.renderer(dt.date(2013, 7, 6), None)
        self.assertEqual('July 6, 2013', out)

    def test_time_german(self):
        activate('de')
        out = self.renderer(dt.time(13, 37, 1), None)
        self.assertEqual('13:37', out)

    def test_time_chinese(self):
        activate('zh')
        out = self.renderer(dt.time(13, 37, 1), None)
        self.assertEqual('1:37 p.m.', out)

    def test_datetime(self):
        out = self.renderer(dt.datetime(2013, 7, 6, 13, 37, 1), None)
        self.assertEqual('July 6, 2013, 1:37 p.m.', out)

    def test_date_as_string(self):
        out = self.renderer('13:37:01', None)
        self.assertEqual('13:37', out)

    # TODO test timezone localization


class TitleRendererTest(TestCase):

    def setUp(self):
        self.renderer = renderers.title_renderer

    def testLowercase(self):
        out = self.renderer('oh hello there!', None)
        self.assertEqual('Oh Hello There!', out)

    def testTitlecase(self):
        out = self.renderer('Oh Hello There!', None)
        self.assertEqual('Oh Hello There!', out)

    def testUppercase(self):
        out = self.renderer('OH HELLO THERE!', None)
        self.assertEqual('Oh Hello There!', out)


class NumberRendererTest(TestCase):

    def setUp(self):
        self.renderer = renderers.number_renderer

    def testInteger(self):
        out = self.renderer(42, None)
        self.assertEqual('42', out)

    def testFloat(self):
        out = self.renderer(42.5, None)
        self.assertEqual('42.5', out)

    def testEndlessFloat(self):
        out = self.renderer(1.0 / 3, None)
        if six.PY2:
            self.assertEqual('0.333333333333', out)
        else:
            self.assertEqual('0.3333333333333333', out)

    def testPlainDecimal(self):
        number = '0.123456789123456789123456789'
        out = self.renderer(Decimal(number), None)
        self.assertEqual(number, out)

    def testFieldDecimal(self):
        field = RendererTestModel._meta.get_field('decimal')
        out = self.renderer(Decimal('0.123456789'), field)
        self.assertEqual('0.12345', out)
