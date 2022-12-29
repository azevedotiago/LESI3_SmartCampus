from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('mac_address','coordinatex','coordinatey','created','group')
    
    
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('device','created','ip_address','valled','stateled', 'valldr', 'valldrnew', 'valpir','statepir')