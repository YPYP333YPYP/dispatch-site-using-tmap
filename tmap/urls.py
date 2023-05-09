from django.urls import path
from .views import GeoInformationView, CenterListCreate, CenterListView, ZoneListCreate, VehicleListCreate, OrderListCreate, DispatchListCreate, CenterListUpdate, delete_CenterList
from . import views

app_name = 'tmap'

urlpatterns = [
    path('geo/', GeoInformationView.as_view(), name='geo'),
    path('center/insert/', CenterListCreate.as_view(), name='center_insert'),
    path('center/update/<int:pk>/', CenterListUpdate.as_view(), name='center_update'),
    path('center/delete/<int:pk>/', delete_CenterList, name='center_update'),
    path('center/get/',CenterListView.as_view()),
    path('zone/insert/', ZoneListCreate.as_view()),
    path('vehicle/insert/', VehicleListCreate.as_view()),
    path('order/insert/', OrderListCreate.as_view()),
    path('dispatch/', DispatchListCreate.as_view()),
    path('map/', views.map_view, name='map_view'),
    path('get_marker_data/',views.get_marker_data)
]

