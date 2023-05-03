from django.db import models


class GeoInformation(models.Model):
    name = models.CharField(max_length=20, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f'[{self.pk}] {self.name}'


class CenterList(models.Model):
    centerId = models.CharField()
    centerName = models.CharField()
    address = models.CharField()

    latitude = models.FloatField()
    longitude = models.FloatField()


class ZonList(models.Model):
    pass


class VehicleList(models.Model):
    pass


class OrderList(models.Model):
    pass


class DispatchList(models.Model):
    pass

