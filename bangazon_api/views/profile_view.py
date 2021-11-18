from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth.models import User

from bangazon_api.serializers import UserSerializer


class ProfileView(ViewSet):
    @action(methods=['GET'], detail=False, url_path="my-profile")
    def my_profile(self, request):
        try:
            serializer = UserSerializer(request.auth.user)
            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['PUT'], detail=False)
    def update(self, request):
        user = request.auth.user
        user.username = request.data['userName']
        user.first_name = request.data['firstName']
        user.last_name = request.data['lastName']
        user.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
