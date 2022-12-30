from rest_framework import serializers
from django.contrib.auth.models import User, Group

# Serializers define the API representation.
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['pk','url','name']

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['pk','url', 'username', 'email', 'is_staff', 'groups']