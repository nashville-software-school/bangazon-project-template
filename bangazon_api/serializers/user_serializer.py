from rest_framework import serializers
from django.contrib.auth.models import User

from bangazon_api.serializers.store_serializer import StoreSerializer


class UserSerializer(serializers.ModelSerializer):
    favorites = StoreSerializer(many=True)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'orders',
                  'favorites', 'store', 'recommended_by')
        depth = 2


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(required=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
