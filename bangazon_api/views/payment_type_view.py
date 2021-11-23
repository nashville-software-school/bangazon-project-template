from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from bangazon_api.models import PaymentType
from bangazon_api.serializers import PaymentTypeSerializer


class PaymentTypeView(ViewSet):
    def list(self, request):
        # TODO: add bug for getting all payment types
        payment_types = PaymentType.objects.filter(user=request.auth.user)
        serializer = PaymentTypeSerializer(payment_types, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            payment_type = PaymentType.objects.create(
                customer=request.auth.user,
                merchant_name=request.data['merchant'],
                acct_number=request.data['acctNumber']
            )
            serializer = PaymentTypeSerializer(payment_type)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            payment_type = PaymentType.objects.get(pk=pk)
            payment_type.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
