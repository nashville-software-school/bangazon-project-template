from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from bangazon_api.models import Store, Favorite
from bangazon_api.serializers import StoreSerializer


class StoreView(ViewSet):
    def create(self, request):
        try:
            store = Store.objects.create(
                user=request.auth.user,
                name=request.data['name'],
                description=request.data['description']
            )
            serializer = StoreSerializer(store)
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            store = Store.objects.get(pk=pk)
            serializer = StoreSerializer(store)
            return Response(serializer.data)
        except Store.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk):
        try:
            store = Store.objects.get(pk=pk)
            store.name = request.data['name']
            store.description = request.data['description']
            store.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except Store.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post', 'delete'], detail=True)
    def favorite_store(self, request, pk):
        try:
            store = Store.objects.get(pk=pk)
        except Store.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        if request.method == "POST":
            favorite = Favorite.objects.create(
                customer=request.auth.user,
                store=store
            )

        if request.method == "DELETE":
            favorite = Favorite.objects.get(
                user=request.auth.user, store=store)
            favorite.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
