from rest_framework import serializers
from bangazon_api.models import Store
from django.contrib.auth.models import User
class StoreUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class StoreSerializer(serializers.ModelSerializer):
    user = StoreUserSerializer()

    class Meta:
        model = Store
        fields = ('id', 'name', 'description', 'user')


class AddStoreSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
