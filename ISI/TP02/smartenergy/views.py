from rest_framework import viewsets
from .models import Device, Log
from .serializers import DeviceSerializer, LogSerializer
from rest_framework.response import Response

# ViewSets define the view behavior.
class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    
    def create(self, request):
        x = DeviceSerializer(data = self.request.data)
        if x.is_valid() == True:
            return Response({'status': x.save()})
        else:
            return Response({'status': 'nok'})
            
        

    # ViewSets define the view behavior.
class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    
    def create(self, request):
        return Response({'status': 'asdas'})