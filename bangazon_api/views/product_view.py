from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from bangazon_api.models import Product, Store, Category, Order
from bangazon_api.models.recommendation import Recommendation
from bangazon_api.serializers import ProductSerializer


class ProductView(ViewSet):
    def create(self, request):
        store = Store.objects.get(seller=request.auth.user)
        category = Category.objects.get(pk=request.data['categoryId'])
        try:
            product = Product.objects.create(
                name=request.data['name'],
                store=store,
                price=request.data['price'],
                description=request.data['description'],
                quantity=request.data['quantity'],
                location=request.data['location'],
                category=category
            )
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        category = Category.objects.get(pk=request.data['categoryId'])

        try:
            product = Product.objects.get(pk=pk)
            product.name = request.data['name']
            product.price = request.data['price']
            product.description = request.data['description']
            product.quantity = request.data['quantity']
            product.location = request.data['location']
            product.category = category
            product.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        # TODO: new feature: filter by category
        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True)
    def add_to_order(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            order = Order.objects.get_or_create(
                user=request.auth.user, completed_on=None, payment_type=None)
            order.products.add(product)
            return Response({'message': 'product added'}, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['delete'], detail=True)
    def remove_from_order(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            order = Order.objects.get(
                user=request.auth.user, completed_on=None)
            order.products.remove(product)
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post', 'delete'], detail=True)
    def recommend(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            customer = User.objects.get(username=request.data['username'])
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        if request.method == "POST":
            recommendation = Recommendation.objects.create(
                product=product,
                recommender=request.auth.user,
                customer=customer
            )

            return Response(None, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            rec_id = request.query_params.get('rec_id', None)
            recommendation = Recommendation.objects.get(pk=rec_id)
            recommendation.delete()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
