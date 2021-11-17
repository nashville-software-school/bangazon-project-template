from datetime import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from bangazon_api.models import Order, PaymentType
from bangazon_api.serializers import OrderSerializer


class OrderView(ViewSet):
    def list(self, request):
        orders = Order.objects.filter(user=request.auth.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            order.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['put'], detail=True)
    def complete(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.auth.user)
            payment_type = PaymentType.objects.get(
                pk=request.data['paymentTypeId'], user=request.auth.user)
            order.payment_type = payment_type
            order.completed_on = datetime.now()
            # TODO: add bug for not saving
            order.save()
            return Response({'message': "Order Completed"})
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
