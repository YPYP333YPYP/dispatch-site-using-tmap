from django.db import models


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

    def __str__(self):
        return f'{self.geo.name}'



class ZonList(models.Model):
    pass


class VehicleList(models.Model):
    pass


class OrderList(models.Model):
    pass


class DispatchList(models.Model):
    pass

