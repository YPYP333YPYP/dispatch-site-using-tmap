from django.urls import path
from .views import GeoInformationView, CenterListCreate, CenterListView, ZoneListCreate, VehicleListCreate, OrderListCreate, DispatchListCreate, CenterListUpdate, delete_CenterList, ZoneListView
from .views import ZoneListUpdate, delete_ZoneList, VehicleListView, VehicleListUpdate, delete_VehicleList
from . import views

app_name = 'tmap'

urlpatterns = [
    path('geo/', GeoInformationView.as_view(), name='geo'),
    path('center/insert/', CenterListCreate.as_view(), name='center_insert'),
    path('center/update/<int:pk>/', CenterListUpdate.as_view(), name='center_update'),
    path('center/delete/<int:pk>/', delete_CenterList, name='center_delete'),
    path('center/', CenterListView.as_view()),
    path('zone/insert/', ZoneListCreate.as_view(), name='zone_insert'),
    path('zone/', ZoneListView.as_view()),
    path('zone/update/<int:pk>/', ZoneListUpdate.as_view()),
    path('zone/delete/<int:pk>/', delete_ZoneList),
    path('vehicle/insert/', VehicleListCreate.as_view(), name='vehicle_insert'),
    path('vehicle/', VehicleListView.as_view()),
    path('vehicle/update/<int:pk>/', VehicleListUpdate.as_view()),
    path('vehicle/delete/<int:pk>/', delete_VehicleList),
    path('order/insert/', OrderListCreate.as_view()),
    path('dispatch/', DispatchListCreate.as_view()),
    path('map/', views.map_view, name='map_view'),
    path('get_marker_data/', views.get_marker_data)
]

