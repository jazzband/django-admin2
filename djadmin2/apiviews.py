# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

from django.utils.encoding import force_str
from rest_framework import fields, generics, serializers
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from . import utils
from .viewmixins import Admin2Mixin

API_VERSION = '0.1'


class Admin2APISerializer(serializers.HyperlinkedModelSerializer):
    _default_view_name = 'admin2:%(app_label)s_%(model_name)s_api_detail'

    pk = fields.ReadOnlyField()
    __unicode__ = fields.ReadOnlyField(source='__str__')

    def get_extra_kwargs(self):
        extra_kwargs = super(Admin2APISerializer, self).get_extra_kwargs()
        extra_kwargs.update({
            'url': {'view_name': self._get_default_view_name(self.Meta.model)}
        })
        return extra_kwargs

    def _get_default_view_name(self, model):
        """
        Return the view name to use if 'view_name' is not specified in 'Meta'
        """
        model_meta = model._meta
        format_kwargs = {
            'app_label': model_meta.app_label,
            'model_name': model_meta.object_name.lower()
        }
        return self._default_view_name % format_kwargs


class Admin2APIMixin(Admin2Mixin):
    model = None
    raise_exception = True

    def get_serializer_class(self):
        if self.serializer_class is None:
            model_class = self.get_model()

            class ModelAPISerilizer(Admin2APISerializer):
                # we need to reset this here, since we don't know anything
                # about the name of the admin instance when declaring the
                # Admin2APISerializer base class
                _default_view_name = ':'.join((
                    self.model_admin.admin.name,
                    '%(app_label)s_%(model_name)s_api_detail'))

                class Meta:
                    model = model_class

            return ModelAPISerilizer
        return super(Admin2APIMixin, self).get_serializer_class()


class IndexAPIView(Admin2APIMixin, APIView):
    apps = None
    registry = None
    app_verbose_names = None
    app_verbose_name = None

    def get_model_data(self, model):
        model_admin = self.registry[model]
        model_options = utils.model_options(model)
        opts = {
            'current_app': model_admin.admin.name,
            'app_label': model_options.app_label,
            'model_name': model_options.object_name.lower(),
        }
        model_url = reverse(
            '%(current_app)s:%(app_label)s_%(model_name)s_api_list' % opts,
            request=self.request,
            format=self.kwargs.get('format'))
        model_options = utils.model_options(model)
        return {
            'url': model_url,
            'verbose_name': force_str(model_options.verbose_name),
            'verbose_name_plural': force_str(model_options.verbose_name_plural),
        }

    def get_app_data(self, app_label, models):
        model_data = []
        for model in models:
            model_data.append(self.get_model_data(model))
        return {
            'app_label': app_label,
            'models': model_data,
            'app_verbose_name': force_str(self.app_verbose_names.get(app_label))
        }

    def get(self, request):
        app_data = []
        for app_label, registry in self.apps.items():
            models = registry.keys()
            app_data.append(self.get_app_data(app_label, models))
        index_data = {
            'version': API_VERSION,
            'apps': app_data,
        }
        return Response(index_data)


class ListCreateAPIView(Admin2APIMixin, generics.ListCreateAPIView):
    pass


class RetrieveUpdateDestroyAPIView(Admin2APIMixin, generics.RetrieveUpdateDestroyAPIView):
    pass
