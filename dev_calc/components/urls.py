from django.urls import path

from . import views

urlpatterns = [
    path('', views.ComponentList.as_view(), name='components-list'),
    path('add/', views.ComponentCreate.as_view(), name='component-add'),
    path('<int:pk>/', views.ComponentUpdate.as_view(), name='component-update'),
    path('<int:pk>', views.ComponentDelete.as_view(), name='component-delete'),
    path('component/<int:pk>', views.ComponentDetail.as_view(), name='component-detail'),
]
