from rest_framework import fields, generics, serializers
from .views import Admin2Mixin


class Admin2APISerializer(serializers.ModelSerializer):
    __str__ = fields.Field(source='__unicode__')


class Admin2APIMixin(Admin2Mixin):
    def get_serializer_class(self):
        if self.serializer_class is None:
            model_class = self.get_model()
            class ModelAPISerilizer(Admin2APISerializer):
                class Meta:
                    model = model_class

            return ModelAPISerilizer
        return super(Admin2APIMixin, self).get_serializer_class()


class ListCreateAPIView(Admin2APIMixin, generics.ListCreateAPIView):
    pass


class RetrieveUpdateDestroyAPIView(Admin2APIMixin, generics.RetrieveUpdateDestroyAPIView):
    pass
