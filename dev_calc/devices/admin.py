from django.contrib import admin

from .models import Device, ComponentDevice, CalcDevice


admin.site.register(Device)
admin.site.register(ComponentDevice)
admin.site.register(CalcDevice)
