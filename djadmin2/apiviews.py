from rest_framework.fields import Field
from rest_framework.generics import ListCreateAPIView
from rest_framework.serializers import ModelSerializer


class Admin2APISerializer(ModelSerializer):
    unicode = Field(source='__unicode__')


class ModelListCreateAPIView(ListCreateAPIView):
    def get_serializer_class(self):
        if self.serializer_class is None:
            class ModelAPISerilizer(Admin2APISerializer):
                class Meta:
                    model = self.model

            return ModelAPISerilizer
        return super(ModelListCreateAPIView, self).get_serializer_class()
