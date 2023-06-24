from django.shortcuts import render, redirect, get_object_or_404
from .models import GeoInformation, CenterList, ZoneList, VehicleList, OrderList, DispatchList
from django.views.generic import CreateView, ListView, UpdateView, TemplateView
import requests
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image


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

# CenterList


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
        centername = center.centerName
        address = geo.name
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


        url = f"https://apis.openapi.sk.com/tmap/staticMap"
        params = {
            'version': 1,
            'appKey': 'lnmQwO8Vzy3E1WkBTNCUv9JWkUEwMQxF4wsCcRjx',
            'width': '500',
            'height': '300',
            'zoom': '12',
            'longitude': longitude,
            'latitude': latitude,
            'markers': str(longitude)+','+str(latitude)
        }
        response = requests.get(url, params=params)

        image = Image.open(ContentFile(response.content))
        filename = f"static_map_{centername}.jpg"
        path = default_storage.save(f'tmap/images/center/{filename}', ContentFile(response.content))
        center.image = path

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
    fields = ['centerName']
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
    fields = ['code', 'name', 'type']
    template_name = 'tmap/zone/zone_insert.html'
    success_url = reverse_lazy('tmap:zone_insert')

    def form_valid(self, form):
        zone = form.save(commit=False)

        name = zone.name
        code = zone.code
        type = zone.type

        if type == "1":
            type="city_do"
        elif type == "2":
            type="gu_gun"
        elif type == "3":
            type="legalDong"
        else:
            type="adminDong"

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
        zone.type = type
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
    fields = ['type', 'name']
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
    fields = ['vehicleId', 'vehicleName', 'vehicleType', 'zoneCode']
    template_name = 'tmap/vehicle/vehicle_insert.html'
    success_url = reverse_lazy('tmap:vehicle_insert')

    def get_context_data(self, **kwargs):
        context = super(VehicleListCreate, self).get_context_data()

        return context

    def form_valid(self, form):
        skill_per = self.request.POST.get('skill_per')

        if skill_per == '':
            skill_per = 0

        form.instance.skillPer = skill_per

        vehicle = form.save(commit=False)
        vehicledetail = vehicle.vehicleType
        weight = int(vehicledetail.weight)
        volume = vehicledetail.volume
        zone = vehicle.zoneCode
        vehicle_type = vehicledetail.type
        vehicleid = vehicle.vehicleId
        vehiclename = vehicle.vehicleName

        zone_code = zone.code

        appkey = "lnmQwO8Vzy3E1WkBTNCUv9JWkUEwMQxF4wsCcRjx"

        url = f"https://apis.openapi.sk.com/tms/vehicleInsert?appKey={appkey}&vehicleId={vehicleid}&vehicleName={vehiclename}&weight={weight}&vehicleType={vehicle_type}&zoneCode={zone_code}&skillPer={skill_per}&volume={volume} "

        headers = {
            "accept": "application/json",
            "appKey": "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5"
        }

        response = requests.get(url, headers=headers)
        response = response.json()
        flag = response["resultCode"]
        vehicle.flag = flag
        vehicle.save()

        alert_script = f"alert('차량 입력 완료!');location.href='{self.success_url}';"
        return HttpResponse(f"<script>{alert_script}</script>")


class VehicleListView(ListView):
    model = VehicleList
    template_name = 'tmap/vehicle/vehicle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicleList_list'] = VehicleList.objects.all()

        return context


class VehicleListUpdate(UpdateView):
    model = VehicleList
    fields = ['vehicleName', 'vehicleType', 'zoneCode','skillPer']
    template_name = 'tmap/vehicle/vehicle_update.html'

    def get_context_data(self, **kwargs):
        context = super(VehicleListUpdate, self).get_context_data()
        return context

    def form_valid(self, form):
        vehicle = form.save(commit=False)
        vehicleid = vehicle.vehicleId
        vehiclename = vehicle.vehicleName
        vehicledetail = vehicle.vehicleType
        weight = vehicledetail.weight
        zone = vehicle.zoneCode
        vehicletype = vehicledetail.type
        skillper = vehicle.skillPer
        volume = vehicledetail.volume
        flag = vehicle.flag

        zone_code = zone.code

        if skillper == '':
            skillper = 0

        appkey = "lnmQwO8Vzy3E1WkBTNCUv9JWkUEwMQxF4wsCcRjx"

        url = f"https://apis.openapi.sk.com/tms/vehicleUpdate?appKey={appkey}&vehicleId={vehicleid}&vehicleName={vehiclename}&weight={weight}&vehicleType={vehicletype}&zoneCode={zone_code}&skillPer={skillper}&volume={volume}"

        headers = {
            "accept": "application/json",
            "appKey": "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5"
        }

        response = requests.get(url, headers=headers)
        response = response.json()

        flag = response["resultCode"]
        vehicle.flag = flag

        vehicle.save()

        return redirect('/tmap/vehicle/')


def delete_VehicleList(request, pk):
    vehicleList = get_object_or_404(VehicleList, pk=pk)
    vehicleid = vehicleList.vehicleId
    appkey = "lnmQwO8Vzy3E1WkBTNCUv9JWkUEwMQxF4wsCcRjx"

    url = f"https://apis.openapi.sk.com/tms/vehicleDelete?appKey={appkey}&deleteFlag=2&vehicleId={vehicleid}"

    headers = {
        "accept": "application/json",
        "appKey": "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5"
    }

    response = requests.get(url, headers=headers)

    vehicleList.delete()
    return redirect('/tmap/vehicle/')


class OrderListCreate(CreateView):
    model = OrderList
    fields = ['orderId', 'orderName', 'geo', 'deliveryWeight', 'zoneCode', 'vehicleType']
    template_name = 'tmap/order/order_insert.html'
    success_url = reverse_lazy('tmap:order_insert')

    def get_context_data(self, **kwargs):
        context = super(OrderListCreate, self).get_context_data()
        return context

    def form_valid(self, form):

        service_time = self.request.POST.get('service_time')
        delivery_volume = self.request.POST.get('delivery_volume')
        if delivery_volume == '':
            delivery_volume = 0

        if service_time == '':
            service_time = 0

        form.instance.serviceTime = service_time
        form.instance.volume = delivery_volume

        order = form.save(commit=False)

        orderid = order.orderId
        ordername = order.orderName
        address = order.geo.name
        latitude = order.geo.latitude
        longitude = order.geo.longitude
        delivery_weight = order.deliveryWeight
        vehicle_type = order.vehicleType
        zonecode = order.zoneCode.code

        appkey = "lnmQwO8Vzy3E1WkBTNCUv9JWkUEwMQxF4wsCcRjx"

        url = f"https://apis.openapi.sk.com/tms/orderInsert?appKey={appkey}&orderId={orderid}&orderName={ordername}&address={address}&latitude={latitude}&longitude={longitude}&vehicleType={vehicle_type}&serviceTime={service_time}&zoneCode={zonecode}&deliveryWeight={delivery_weight}&deliveryVolume={delivery_volume}"


        headers = {
            "accept": "application/json",
            "appKey": "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5"
        }

        response = requests.get(url, headers=headers)
        response = response.json()
        flag = response["resultCode"]
        order.flag = flag
        order.save()

        alert_script = f"alert('배송지 입력 완료!');location.href='{self.success_url}';"
        return HttpResponse(f"<script>{alert_script}</script>")


class OrderListView(ListView):
    model = OrderList
    template_name = 'tmap/order/order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orderList_list'] = OrderList.objects.all()
        return context


class OrderListUpdate(UpdateView):
    model = OrderList
    fields = ['orderName', 'geo', 'serviceTime', 'deliveryWeight','deliveryVolume','zoneCode','vehicleType']
    template_name = 'tmap/order/order_update.html'

    def get_context_data(self, **kwargs):
        context = super(OrderListUpdate, self).get_context_data()
        return context

    def form_valid(self, form):
        order = form.save(commit=False)
        geo = order.geo
        orderid = order.orderId
        ordername = order.orderName
        address = geo.name
        latitude = geo.latitude
        longitude = geo.longitude
        servicetime = order.serviceTime
        deliveryweight = order.deliveryWeight
        deliveryvolume = order.deliveryVolume
        zonecode = order.zoneCode
        flag = order.flag

        if servicetime == '':
            servicetime = 0

        appkey = "lnmQwO8Vzy3E1WkBTNCUv9JWkUEwMQxF4wsCcRjx"


        url = f"https://apis.openapi.sk.com/tms/orderUpdate?appKey={appkey}&orderId={orderid}&orderName={ordername}&address={address}&latitude={latitude}&longitude={longitude}&serviceTime={servicetime}&deliveryWeight={deliveryweight}&deliveryVolume={deliveryvolume}&zoneCode={zonecode}"

        headers = {
            "accept": "application/json",
            "appKey": "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5"
        }

        response = requests.get(url, headers=headers)
        response = response.json()

        flag = response["resultCode"]
        order.flag = flag

        order.save()

        return redirect('/tmap/order/')


def delete_OrderList(request, pk):
    orderList = get_object_or_404(OrderList, pk=pk)
    orderid = orderList.orderId
    appkey = "lnmQwO8Vzy3E1WkBTNCUv9JWkUEwMQxF4wsCcRjx"

    url = f"https://apis.openapi.sk.com/tms/orderDelete?appKey={appkey}&deleteFlag=2&orderId={orderid}"

    headers = {
        "accept": "application/json",
        "appKey": "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5"
    }

    response = requests.get(url, headers=headers)

    orderList.delete()
    return redirect('/tmap/order/')


class DispatchListCreate(CreateView):
    model = DispatchList
    fields = ['startTime']
    template_name = 'tmap/dispatch/dispatch.html'

    def form_valid(self, form):
        option_type = self.request.POST.get('option_type')
        equalization_type = self.request.POST.get('equalization_type')
        allocation_type = self.request.POST.get('allocation_type')
        orderListId = self.request.POST.get("orderListId")
        vehicleListId = self.request.POST.get("vehicleListId")
        dispatch = form.save(commit=False)
        starttime = dispatch.startTime

        orderlist = OrderList.objects.filter(orderId=orderListId).first()
        vehiclelist = VehicleList.objects.filter(vehicleId=vehicleListId).first()


        appkey = "lnmQwO8Vzy3E1WkBTNCUv9JWkUEwMQxF4wsCcRjx"

        url = f"https://apis.openapi.sk.com/tms/allocation?appKey={appkey}&allocationType={allocation_type}&orderIdList={orderListId}&vehicleIdList={vehicleListId}&startTime={starttime}&optionType={option_type}&equalizationType={equalization_type}"

        headers = {
            "accept": "application/json",
            "appKey": "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5"
        }

        response = requests.get(url, headers=headers)
        response = response.json()
        mappingkey = response["mappingKey"]

        flag = response["resultCode"]
        message = response["resultMessage"]

        if flag != "200":
            alert_script = f"alert('{message}.!');location.href='{self.success_url}';"
            return HttpResponse(f"<script>{alert_script}</script>")
        else:
            url = f"https://apis.openapi.sk.com/tms/allocationData?appKey={appkey}&mappingKey={mappingkey}&routeYn=N"

            headers = {
                "accept": "application/json",
                "appKey": "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5"
            }

            response = requests.get(url, headers=headers)
            response = response.json()

            expectedArrivalTime = response["vehicleList"]["orderList"][0]["expectedArrivalTime"]
            expectedDepartureTime = response["vehicleList"]["orderList"][0]["expectedDepartureTime"]
            end_latitude = response["vehicleList"]["orderList"][0]["latitude"]
            end_longitude = response["vehicleList"]["orderList"][0]["longitude"]
            vehicleName = response["vehicleList"]["vehicleName"]
            orderName = response["vehicleList"]["orderList"][0]["orderName"]
            address = response["vehicleList"]["orderList"][0]["address"]

        center = CenterList.objects.filter(flag=200)
        start_latitude = center.geo.latitude
        start_longitude = center.geo.longitude

        dispatchList = DispatchList(orderList=orderlist, vehicleList=vehiclelist, startTime=starttime, allocationType=allocation_type,
                                    optionType=option_type, equalizationType=equalization_type, mappingKey=mappingkey, flag=flag,
                                    expectedArrivalTime=expectedArrivalTime, expectedDepartureTime=expectedDepartureTime,
                                    start_latitude=start_latitude, start_longitude=start_longitude, end_latitude=end_latitude, end_longitude=end_longitude,
                                    vehicleName=vehicleName, orderName=orderName, address=address)
        dispatchList.save()

        return redirect('/tmap/dispatch/')


class MainListView(TemplateView):
    template_name = 'tmap/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orderList'] = OrderList.objects.all()
        context['centerList'] = CenterList.objects.all()
        context['vehicleList'] = VehicleList.objects.all()
        context['zoneList'] = ZoneList.objects.all()
        return context


def get_marker_data(request):
    locations = OrderList.objects.all()

    marker_data = []

    for location in locations:
        lat = location.geo.latitude
        lng = location.geo.longitude
        marker_data.append({
            'position': f'new Tmapv2.LatLng({lat}, {lng})',
            'icon': 'http://tmapapi.sktelecom.com/upload/tmap/marker/pin_r_m_s.png',
            'iconSize': 'new Tmapv2.Size(24, 38)',
        })

    return JsonResponse({'marker_data': marker_data})



# todo
"""
    1. 정상적으로 배차 나오는지 확인하기
    2. 각 model CRUD에서 유효성 검사 및 프론트 엔드 부분 내용 추가하기
    3. 배차 결과 페이지 작성하기
"""