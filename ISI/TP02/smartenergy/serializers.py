from rest_framework import serializers
from .models import Device, Log

# Serializers define the API representation.
class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    
    
    class Meta:
        model = Device
        fields = ['created','mac_address', 'coordinatex' , 'coordinatey','group']
        
    def create(self, validated_data):
        return Device.objects.create(**validated_data)

# Serializers define the API representation.
class LogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = ['created', 
                  'ip_address', 
                  'valled', 
                  'stateled', 
                  'valldr', 
                  'valldrnew',
                  'valpir',
                  'statepir'
                  ]