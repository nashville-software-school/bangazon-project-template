from rest_framework import serializers
from bangazon_api.models import Store
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        depth = 1
