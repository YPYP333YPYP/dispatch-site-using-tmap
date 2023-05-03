from django.urls import path
from .views import GeoInformationView, CenterListCreate, CenterListView

urlpatterns = [
    path('geo/', GeoInformationView.as_view()),
    path('center/insert/', CenterListCreate.as_view()),
    path('center/get/',CenterListView.as_view()),
]