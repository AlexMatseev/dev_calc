from django.urls import path

from . import views

urlpatterns = [
    path('', views.DeviceList.as_view(), name='device-list'),
    path('devices/add/', views.DeviceCreate.as_view(), name='device-add'),
    path('devices/<int:pk>', views.DeviceUpdate.as_view(), name='device-update'),
    path('devices/<int:pk>', views.DeviceDelete.as_view(), name='device-delete'),
    path('calculations/', views.CalcDeviceList.as_view(), name='calc_device-list'),
    path('calculations/create', views.CalcDeviceCreate.as_view(), name='calc_device-add'),
    path('calculations/<int:pk>', views.CalcDeviceDetail.as_view(), name='calc_device-detail'),
]
