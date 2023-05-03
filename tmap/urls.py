from django.urls import path
from .views import GeoInformationView

urlpatterns = [
    path('geo/', GeoInformationView.as_view())
]