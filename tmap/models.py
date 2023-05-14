from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class GeoInformation(models.Model):
    name = models.CharField(max_length=20, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return f'{self.name}'


class CenterList(models.Model):
    centerId = models.CharField(max_length=100)
    centerName = models.CharField(max_length=100)
    geo = models.ForeignKey(GeoInformation, null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='tmap/images/center/', blank=True)
    flag = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f'{self.pk} + {self.centerId}'

    def get_absolute_url(self):
        return f'/tmap/center/{self.pk}'


class ZoneList(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True)
    flag = models.CharField(max_length=10, null=True)
    type = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return f'/tmap/zone/{self.pk}'


class VehicleList(models.Model):
    vehicleId = models.CharField(max_length=100, null=True)
    vehicleName = models.CharField(max_length=100, null=True)
    weight = models.IntegerField(null=True)
    vehicleType = models.CharField(max_length=100, default="02")
    zoneCode = models.CharField(max_length=10, null=True)
    skillPer = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], null=True)
    volume = models.IntegerField(null=True)
    flag = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f'{self.vehicleId}'

    def get_absolute_url(self):
        return f'/tmap/vehicle/{self.pk}'


class OrderList(models.Model):
    orderId = models.CharField(max_length=100, null=True)
    orderName = models.CharField(max_length=100, null=True)
    geo = models.ForeignKey(GeoInformation, null=True, blank=True, on_delete=models.CASCADE)
    vehicleType = models.CharField(max_length=100, default="02")
    serviceTime = models.IntegerField(null=True)
    zoneCode = models.CharField(max_length=100, null=True)
    deliveryWeight = models.CharField(max_length=100, null=True)
    deliveryVolume = models.CharField(max_length=100, null=True)
    updateDate = models.DateTimeField(null=True)
    flag = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f'{self.orderId}'

    def get_absolute_url(self):
        return f'/tmap/order/{self.pk}'


class DispatchList(models.Model):
    orderList = models.ForeignKey(OrderList, blank=True, null=True, on_delete=models.CASCADE)
    vehicleList = models.ForeignKey(VehicleList, blank=True, null=True, on_delete=models.CASCADE)
    allocationType = models.CharField(max_length=10, null=True, blank=False)
    startTime = models.CharField(max_length=10, blank=False, null=True)
    optionType = models.CharField(max_length=10, null=True)
    equalizationType = models.CharField(max_length=10, null=True)
    mappingKey = models.CharField(max_length=100, null=True)
    flag = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f'{self.orderList}'


class DispatchListResult(models.Model):
    orderList = models.ForeignKey(OrderList, blank=False, on_delete=models.CASCADE)
    vehicleList = models.ForeignKey(VehicleList, blank=False, on_delete=models.CASCADE)
    expectedArrivalTime = models.DateTimeField(null=True)
    expectedDepartureTime = models.DateTimeField(null=True)
    start_latitude = models.FloatField(default=0.0)
    start_longitude = models.FloatField(default=0.0)
    end_latitude = models.FloatField(default=0.0)
    end_longitude = models.FloatField(default=0.0)
    vehicleName = models.CharField(max_length=100, null=True)
    orderName = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    flag = models.CharField(max_length=10, null=True)
