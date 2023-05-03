from django.shortcuts import render,redirect
from .models import GeoInformation
from django.views.generic import CreateView
import requests
from urllib import parse


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
