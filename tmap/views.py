from django.shortcuts import render, redirect, get_object_or_404
from .models import GeoInformation, CenterList, ZoneList, VehicleList, OrderList, DispatchList
from django.views.generic import CreateView, ListView, UpdateView
import requests
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy


class GeoInformationView(CreateView):
    model = GeoInformation
    fields = ['name']
    template_name = 'tmap/geo.html'
    success_url = reverse_lazy('tmap:geo')

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

        alert_script = f"alert('센터 입력 완료!');location.href='{self.success_url}';"

        return HttpResponse(f"<script>{alert_script}</script>")


class CenterListCreate(CreateView):
    model = CenterList
    fields = ['centerId', 'centerName', 'geo']
    template_name = 'tmap/center/center_insert.html'
    success_url = reverse_lazy('tmap:center_insert')

    def form_valid(self, form):
        center = form.save(commit=False)
        geo = center.geo

        latitude = geo.latitude
        longitude = geo.longitude
        centerid = center.centerId
        centername = center.centerName.encode('utf-8')
        address = geo.name.encode('utf-8')
        appkey = "lnmQwO8Vzy3E1WkBTNCUv9JWkUEwMQxF4wsCcRjx"

        url = f'https://apis.openapi.sk.com/tms/centerInsert?appKey={appkey}&centerId={centerid}&centerName={centername}&address={address}&latitude={latitude}&longitude={longitude}'

        headers = {
            "accept": "application/json",
            "appKey": "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5"
        }

        response = requests.get(url, headers=headers)
        response = response.json()

        flag = response["resultCode"]
        center.flag = flag

        center.save()
        alert_script = f"alert('센터 입력 완료!');location.href='{self.success_url}';"
        return HttpResponse(f"<script>{alert_script}</script>")


class CenterListView(ListView):
    model = CenterList
    template_name = 'tmap/center/center.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['centerList_list'] = CenterList.objects.all().order_by('flag')
        return context


class CenterListUpdate(UpdateView):
    model = CenterList
    fields = ['centerName', 'geo']
    template_name = 'tmap/center/center_update.html'

    def get_context_data(self, **kwargs):
        context = super(CenterListUpdate, self).get_context_data()
        return context

    def form_valid(self, form):

        center = form.save(commit=False)
        geo = center.geo

        latitude = geo.latitude
        longitude = geo.longitude
        centerid = center.centerId
        centername = center.centerName.encode('utf-8')
        address = geo.name.encode('utf-8')
        flag = center.flag
        appkey = "lnmQwO8Vzy3E1WkBTNCUv9JWkUEwMQxF4wsCcRjx"
        if flag == "200":
            url = f'https://apis.openapi.sk.com/tms/centerUpdate?appKey={appkey}&centerId={centerid}&centerName={centername}&address={address}&latitude={latitude}&longitude={longitude}'

            headers = {
                "accept": "application/json",
                "appKey": "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5"
            }

            response = requests.get(url, headers=headers)
            response = response.json()

            flag = response["resultCode"]
            center.flag = flag

        center.save()

        return redirect('/tmap/center/')


def delete_CenterList(request, pk):
    centerList = get_object_or_404(CenterList, pk=pk)
    centerid = centerList.centerId
    appkey = "lnmQwO8Vzy3E1WkBTNCUv9JWkUEwMQxF4wsCcRjx"
    url = f"https://apis.openapi.sk.com/tms/centerDelete?appKey={appkey}&centerId={centerid}"

    headers = {
        "accept": "application/json",
        "appKey": "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5"
    }

    response = requests.get(url, headers=headers)

    centerList.delete()
    return redirect('/tmap/center/')


class ZoneListCreate(CreateView):
    model = ZoneList
    fields = ['code', 'name']
    template_name = 'tmap/zone/zone_insert.html'
    success_url = reverse_lazy('tmap:zone_insert')

    def form_valid(self, form):
        zone = form.save(commit=False)

        name = zone.name
        code = zone.code
        appkey = "lnmQwO8Vzy3E1WkBTNCUv9JWkUEwMQxF4wsCcRjx"
        url = f'https://apis.openapi.sk.com/tms/zoneInsert?appKey={appkey}&code={code}&name={name}'

        headers = {
            "accept": "application/json",
            "appKey": "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5"
        }

        response = requests.get(url, headers=headers)
        response = response.json()

        flag = response["resultCode"]
        zone.flag = flag

        zone.save()

        alert_script = f"alert('권역 입력 완료!');location.href='{self.success_url}';"
        return HttpResponse(f"<script>{alert_script}</script>")


class ZoneListView(ListView):
    model = ZoneList
    template_name = 'tmap/zone/zone.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['zoneList_list'] = ZoneList.objects.all()
        return context


class ZoneListUpdate(UpdateView):
    model = ZoneList
    fields = ['name']
    template_name = 'tmap/zone/zone_update.html'

    def get_context_data(self, **kwargs):
        context = super(ZoneListUpdate, self).get_context_data()
        return context

    def form_valid(self, form):

        zone = form.save(commit=False)
        name = zone.name
        code = zone.code

        flag = zone.flag
        appkey = "lnmQwO8Vzy3E1WkBTNCUv9JWkUEwMQxF4wsCcRjx"

        if flag == "200":
            url = f"https://apis.openapi.sk.com/tms/zoneUpdate?appKey={appkey}&code={code}&name={name}"

            headers = {
                "accept": "application/json",
                "appKey": "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5"
            }

            response = requests.get(url, headers=headers)
            response = response.json()

            flag = response["resultCode"]
            zone.flag = flag

        zone.save()

        return redirect('/tmap/zone/')


def delete_ZoneList(request, pk):
    zoneList = get_object_or_404(ZoneList, pk=pk)
    code = zoneList.code
    appkey = "lnmQwO8Vzy3E1WkBTNCUv9JWkUEwMQxF4wsCcRjx"
    url = f"https://apis.openapi.sk.com/tms/zoneDelete?appKey={appkey}&code={code}"

    headers = {
        "accept": "application/json",
        "appKey": "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5"
    }

    response = requests.get(url, headers=headers)

    zoneList.delete()
    return redirect('/tmap/zone/')


class VehicleListCreate(CreateView):
    model = VehicleList
    fields = ['vehicleId', 'vehicleName', 'weight']
    template_name = 'tmap/vehicle/vehicle_insert.html'

    def form_valid(self, form):

        vehicle_type = self.request.POST.get('vehicle_type')
        zone_code = self.request.POST.get('zone_code')
        skill_per = self.request.POST.get('skill_per')
        if skill_per == '':
            skill_per = 0
        volume = self.request.POST.get('volume')
        if volume == '':
            volume = 0

        if vehicle_type == "상온":
            vehicle_type = "01"
        elif vehicle_type == "냉장/냉동":
            vehicle_type = "02"
        else:
            vehicle_type = "99"

        form.instance.vehicleType = vehicle_type
        form.instance.zoneCode = zone_code
        form.instance.skillPer = skill_per
        form.instance.volume = volume

        vehicle = form.save(commit=False)

        vehicleid = vehicle.vehicleId
        vehiclename = vehicle.vehicleName
        weight = vehicle.weight
        appkey = "lnmQwO8Vzy3E1WkBTNCUv9JWkUEwMQxF4wsCcRjx"

        url = f"https://apis.openapi.sk.com/tms/vehicleInsert?appKey={appkey}&vehicleId={vehicleid}&vehicleName={vehiclename}&weight={weight}&vehicleType={vehicle_type}&zoneCode={zone_code}&skillPer={skill_per}&volume={volume}"

        headers = {
            "accept": "application/json",
            "appKey": "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5"
        }

        response = requests.get(url, headers=headers)
        response = response.json()
        flag = response["resultCode"]
        vehicle.flag = flag
        vehicle.save()

        return redirect('/tmap/vehicle/insert')


class OrderListCreate(CreateView):
    model = OrderList
    fields = ['orderId', 'orderName', 'geo', 'deliveryWeight']
    template_name = 'tmap/order/order_insert.html'

    def form_valid(self, form):

        vehicle_type = self.request.POST.get('vehicle_type')
        service_time = self.request.POST.get('service_time')
        zone_code = self.request.POST.get('zone_code')
        delivery_volume = self.request.POST.get('delivery_volume')
        if delivery_volume == '':
            delivery_volume = 0

        if vehicle_type == "상온":
            vehicle_type = "01"
        elif vehicle_type == "냉장/냉동":
            vehicle_type = "02"
        else:
            vehicle_type = "99"

        form.instance.vehicleType = vehicle_type
        form.instance.zoneCode = zone_code
        form.instance.serviceTime = service_time
        form.instance.volume = delivery_volume


        order = form.save(commit=False)

        orderid = order.orderId
        ordername = order.orderName
        address = order.geo.name
        latitude = order.geo.latitude
        longitude = order.geo.longitude
        delivery_weight = order.deliveryWeight

        appkey = "lnmQwO8Vzy3E1WkBTNCUv9JWkUEwMQxF4wsCcRjx"

        url = f"https://apis.openapi.sk.com/tms/orderInsert?appKey={appkey}&orderId={orderid}&orderName={ordername}&address={address}&latitude={latitude}&longitude={longitude}&vehicleType={vehicle_type}&serviceTime={service_time}&zoneCode={zone_code}&deliveryWeight={delivery_weight}&deliveryVolume={delivery_volume}"

        headers = {
            "accept": "application/json",
            "appKey": "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5"
        }

        response = requests.get(url, headers=headers)
        response = response.json()
        flag = response["resultCode"]
        order.flag = flag
        order.save()

        return redirect('/tmap/order/insert')


class DispatchListCreate(CreateView):
    model = DispatchList
    fields = ['orderList', 'vehicleList', 'startTime']
    template_name = 'tmap/dispatch/dispatch.html'

    def form_valid(self, form):
        option_type = self.request.POST.get('option_type')
        equalization_type = self.request.POST.get('equalization_type')

        dispatch = form.save(commit=False)

        orderlist = dispatch.orderList
        vehiclelist = dispatch.vehicleList
        starttime = dispatch.startTime

        appkey = "lnmQwO8Vzy3E1WkBTNCUv9JWkUEwMQxF4wsCcRjx"

        url = f"https://apis.openapi.sk.com/tms/allocation?appKey={appkey}&allocationType=1&orderIdList={orderlist}&vehicleIdList={vehiclelist}&startTime={starttime}&optionType={option_type}&equalizationType={equalization_type}"

        headers = {
            "accept": "application/json",
            "appKey": "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5"
        }

        response = requests.get(url, headers=headers)
        response = response.json()
        mappingkey = response["mappingKey"]

        flag = response["resultCode"]
        dispatchList = DispatchList(orderList=orderlist, vehicleList=vehiclelist, startTime=starttime,
                                    optionType=option_type, equalizationType=equalization_type, mappingKey=mappingkey, flag=flag)
        dispatchList.save()

        return redirect('/tmap/dispatch/')


def get_marker_data(request):

    locations = GeoInformation.objects.all()


    marker_data = []
    for location in locations:
        lat = location.latitude
        lng = location.longitude
        marker_data.append({
            'position': f'new Tmapv2.LatLng({lat}, {lng})',
            'icon': 'http://tmapapi.sktelecom.com/upload/tmap/marker/pin_r_m_s.png',
            'iconSize': 'new Tmapv2.Size(24, 38)',
        })

    # 변환된 위치 정보를 JSON 형태로 반환합니다.
    return JsonResponse({'marker_data': marker_data})

# views.py


def map_view(request):
    return render(request, 'tmap/main.html')
