from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from .serializers import GroupSerializer, UserSerializer

# ViewSets define the view behavior.
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    # ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer