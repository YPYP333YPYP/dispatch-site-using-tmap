from django.contrib import admin
from .models import GeoInformation, CenterList, VehicleList, OrderList, DispatchList

admin.site.register(GeoInformation)

admin.site.register(CenterList)

admin.site.register(VehicleList)

admin.site.register(OrderList)

admin.site.register(DispatchList)