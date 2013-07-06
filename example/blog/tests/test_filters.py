# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from ..models import Post

import djadmin2
import djadmin2.filters as djadmin2_filters

import django_filters


class PostAdminSimple(djadmin2.ModelAdmin2):
    list_filter = ['published', ]


class PostAdminWithFilterInstances(djadmin2.ModelAdmin2):
    list_filter = [
        django_filters.BooleanFilter(name='published'),
    ]


class FS(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['published']


class PostAdminWithFilterSetInst(djadmin2.ModelAdmin2):
    list_filter = FS


class ListFilterBuilderTest(TestCase):

    def setUp(self):
        self.rf = RequestFactory()

    def test_filter_building(self):
        Post.objects.create(title="post_1_title", body="body")
        Post.objects.create(title="post_2_title", body="another body")
        request = self.rf.get(reverse("admin2:dashboard"))
        list_filter_inst = djadmin2_filters.build_list_filter(
            request,
            PostAdminSimple,
            Post.objects.all(),
        )
        self.assertTrue(
            issubclass(list_filter_inst.__class__, django_filters.FilterSet)
        )
        self.assertEqual(
            list_filter_inst.filters['published'].widget,
            djadmin2_filters.NullBooleanLinksWidget,
        )
        list_filter_inst = djadmin2_filters.build_list_filter(
            request,
            PostAdminWithFilterInstances,
            Post.objects.all(),
        )
        self.assertNotEqual(
            list_filter_inst.filters['published'].widget,
            djadmin2_filters.NullBooleanLinksWidget,
        )
        list_filter_inst = djadmin2_filters.build_list_filter(
            request,
            PostAdminWithFilterSetInst,
            Post.objects.all(),
        )
        self.assertTrue(isinstance(list_filter_inst, FS))
