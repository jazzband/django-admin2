from rest_framework import fields, generics, serializers


class Admin2APISerializer(serializers.ModelSerializer):
    unicode = fields.Field(source='__unicode__')


class Admin2APIMixin(object):
    modeladmin = None

    def get_serializer_class(self):
        if self.serializer_class is None:
            class ModelAPISerilizer(Admin2APISerializer):
                class Meta:
                    model = self.model

            return ModelAPISerilizer
        return super(ModelListCreateAPIView, self).get_serializer_class()


class ModelListCreateAPIView(Admin2APIMixin, generics.ListCreateAPIView):
    pass


class ModelRetrieveUpdateDestroyAPIView(Admin2APIMixin, generics.RetrieveUpdateDestroyAPIView):
    pass
