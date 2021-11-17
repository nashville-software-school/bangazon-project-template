from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from bangazon_api.models import Category
from bangazon_api.serializers import CategorySerializer


class CategoryView(ViewSet):
    def create(self, request):
        try:
            category = Category.objects.create(
                name=request.data['name']
            )
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
