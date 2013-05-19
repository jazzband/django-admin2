from django.utils.encoding import force_str
from rest_framework import fields, generics, serializers
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from .views import Admin2Mixin

API_VERSION = '0.1'


class Admin2APISerializer(serializers.HyperlinkedModelSerializer):
    _default_view_name = 'admin2:%(app_label)s_%(model_name)s_api-detail'

    pk = fields.Field(source='pk')
    __str__ = fields.Field(source='__unicode__')


class Admin2APIMixin(Admin2Mixin):
    def get_serializer_class(self):
        if self.serializer_class is None:
            model_class = self.get_model()

            class ModelAPISerilizer(Admin2APISerializer):
                # we need to reset this here, since we don't know anything
                # about the name of the admin instance when declaring the
                # Admin2APISerializer base class
                _default_view_name = ':'.join((
                    self.modeladmin.admin.name,
                    '%(app_label)s_%(model_name)s_api-detail'))

                class Meta:
                    model = model_class

            return ModelAPISerilizer
        return super(Admin2APIMixin, self).get_serializer_class()


class IndexAPIView(Admin2APIMixin, APIView):
    apps = None
    registry = None

    def get_model_data(self, model):
        modeladmin = self.registry[model]
        opts = {
            'current_app': modeladmin.admin.name,
            'app_label': model._meta.app_label,
            'model_name': model._meta.object_name.lower(),
        }
        model_url = reverse(
            '%(current_app)s:%(app_label)s_%(model_name)s_api-list' % opts,
            request=self.request,
            format=self.kwargs.get('format'))
        return {
            'url': model_url,
            'verbose_name': force_str(model._meta.verbose_name),
            'verbose_name_plural': force_str(model._meta.verbose_name_plural),
        }

    def get_app_data(self, app_label, models):
        model_data = []
        for model in models:
            model_data.append(self.get_model_data(model))
        return {
            'app_label': app_label,
            'models': model_data,
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
