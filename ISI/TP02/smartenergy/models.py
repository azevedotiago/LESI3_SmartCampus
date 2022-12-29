
from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class Device(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    mac_address = models.CharField(max_length=30)
    coordinatex = models.CharField(max_length=30)
    coordinatey = models.CharField(max_length=30)
    
    def __str__(self):
        return self.mac_address
    
class Log(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=30)
    valled = models.IntegerField()
    stateled = models.IntegerField()
    valldr = models.IntegerField()
    valldrnew = models.IntegerField()
    valpir = models.IntegerField()
    statepir = models.IntegerField()
    
    def __str__(self):
        return self.ip_address