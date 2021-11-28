from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from bangazon_api.models import Product, Store, Category, Order, Rating, Recommendation
from bangazon_api.serializers import (
    ProductSerializer, CreateProductSerializer, MessageSerializer,
    AddProductRatingSerializer, AddRemoveRecommendationSerializer)


class ProductView(ViewSet):
    @swagger_auto_schema(
        request_body=CreateProductSerializer,
        responses={
            201: openapi.Response(
                description="Returns the created product",
                schema=ProductSerializer()
            ),
            400: openapi.Response(
                description="Validation Error",
                schema=MessageSerializer()
            )
        }
    )
    def create(self, request):
        """Create a new product for the current user's store"""
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

    @swagger_auto_schema(
        request_body=CreateProductSerializer,
        responses={
            204: openapi.Response(
                description="No Content",
            ),
            400: openapi.Response(
                description="Validation Error",
                schema=MessageSerializer()
            ),
            404: openapi.Response(
                description="The product was not found",
                schema=MessageSerializer()
            )
        }
    )
    def update(self, request, pk):
        """Update a product"""
        category = Category.objects.get(pk=request.data['categoryId'])

        try:
            product = Product.objects.get(pk=pk, store__user=request.auth.user)
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

    @swagger_auto_schema(
        responses={
            204: openapi.Response(
                description="No Content",
            ),
            404: openapi.Response(
                description="The product was not found",
                schema=MessageSerializer()
            )
        })
    def delete(self, request, pk):
        """Delete a product"""
        try:
            product = Product.objects.get(pk=pk, store__user=request.auth.user)
            product.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="The list of products",
                schema=ProductSerializer(many=True)
            )
        })
    def list(self, request):
        """Get a list of all products"""
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="The requested product",
                schema=ProductSerializer()
            ),
            404: openapi.Response(
                description="Product not found",
                schema=MessageSerializer()
            ),
        }
    )
    def retrieve(self, request, pk):
        """Get a single product"""
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        method='POST',
        responses={
            201: openapi.Response(
                description="Returns message that product was added to order",
                schema=MessageSerializer()
            ),
            404: openapi.Response(
                description="Product not found",
                schema=MessageSerializer()
            ),
        }
    )
    @action(methods=['post'], detail=True)
    def add_to_order(self, request, pk):
        """Add a product to the current users open order"""
        try:
            product = Product.objects.get(pk=pk)
            order = Order.objects.get_or_create(
                user=request.auth.user, completed_on=None, payment_type=None)
            order.products.add(product)
            return Response({'message': 'product added'}, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        method='DELETE',
        responses={
            201: openapi.Response(
                description="Returns message that product was deleted from the order",
                schema=MessageSerializer()
            ),
            404: openapi.Response(
                description="Either the Product or Order was not found",
                schema=MessageSerializer()
            ),
        }
    )
    @action(methods=['delete'], detail=True)
    def remove_from_order(self, request, pk):
        """Remove a product from the users open order"""
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

    @swagger_auto_schema(
        method='DELETE',
        request_body=AddRemoveRecommendationSerializer(),
        responses={
            204: openapi.Response(
                description="No content, the recommendation was deleted",
            ),
            404: openapi.Response(
                description="Either the Product or User was not found",
                schema=MessageSerializer()
            ),
        }
    )
    @swagger_auto_schema(
        method='POST',
        request_body=AddRemoveRecommendationSerializer(),
        responses={
            201: openapi.Response(
                description="No content, the recommendation was added",
            ),
            404: openapi.Response(
                description="Either the Product or User was not found",
                schema=MessageSerializer()
            ),
        }
    )
    @action(methods=['post', 'delete'], detail=True)
    def recommend(self, request, pk):
        """Add or remove a recommendation for a product to another user"""
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
            recommendation = Recommendation.objects.get(
                product=product,
                recommender=request.auth.user,
                customer=customer
            )
            recommendation.delete()

            return Response(None, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        method='POST',
        request_body=AddProductRatingSerializer(),
        responses={
            201: openapi.Response(
                description="No content, the rating was added",
            ),

        }
    )
    @action(methods=['post'], detail=True, url_path='rate-product')
    def rate_product(self, request, pk):
        """Rate a product"""
        product = Product.objects.get(pk=pk)

        try:
            rating = Rating.objects.get(
                user=request.auth.user, product=product)
            rating.score = request.data['score']
            rating.save()
        except Rating.DoesNotExist:
            rating = Rating.objects.create(
                user=request.auth.user,
                product=product,
                score=request.data['score']
            )

        return Response({'message': 'Rating added'}, status=status.HTTP_201_CREATED)
