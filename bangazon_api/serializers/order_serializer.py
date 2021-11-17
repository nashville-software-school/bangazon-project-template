from rest_framework import serializers
from bangazon_api.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'products', 'created_on', 'completed_on')
        depth = 1
