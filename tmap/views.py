from django.shortcuts import render,redirect
from .models import GeoInformation, CenterList
from django.views.generic import CreateView, ListView
import requests


class GeoInformationView(CreateView):
    model = GeoInformation
    fields = ['name']
    template_name = 'tmap/geo.html'

    def form_valid(self, form):
        name = form.cleaned_data['name']

        headers = {
            "Accept": "application/json"
        }
        info = {

            "coordType": "WGS84GEO",
            "fullAddr": name,
        }

        url = f'https://apis.openapi.sk.com/tmap/geo/fullAddrGeo?&coordType={info["coordType"]}&fullAddr={info["fullAddr"]}&appKey=lnmQwO8Vzy3E1WkBTNCUv9JWkUEwMQxF4wsCcRjx'

        response = requests.get(url, headers=headers)

        response = response.json()
        latitude = response["coordinateInfo"]["coordinate"][0]["lat"]
        if latitude == '':
            latitude = response["coordinateInfo"]["coordinate"][0]["newLat"]

        longitude = response["coordinateInfo"]["coordinate"][0]["lon"]
        if longitude == '':
            longitude = response["coordinateInfo"]["coordinate"][0]["newLon"]

        geo = GeoInformation(name=name, latitude=latitude or None, longitude=longitude or None)

        geo.save()
        return redirect('/tmap/geo')


class CenterListCreate(CreateView):
    model = CenterList
    fields = ['centerId', 'centerName', 'geo']
    template_name = 'tmap/center.html'

    def form_valid(self, form):
        center = form.save(commit=False)
        geo = center.geo
        center.save()

        latitude = geo.latitude
        longitude = geo.longitude
        centerid = center.centerId
        centername = center.centerName
        address = geo.name

        url = f'https://apis.openapi.sk.com/tms/centerInsert?appKey=lnmQwO8Vzy3E1WkBTNCUv9JWkUEwMQxF4wsCcRjx&centerId={centerid}&centerName={centername}&address={address}&latitude={latitude}&longitude={longitude}'

        headers = {
            "accept": "application/json",
            "appKey": "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5"
        }

        response = requests.get(url, headers=headers)

        return redirect('/tmap/center')


class CenterListView(ListView):
    model = CenterList

    template_name = 'tmap/center_get.html'

    def get_context_data(self, **kwargs):
        context = super(CenterListView, self).get_context_data()
        return context




