# Generated by Django 4.1.7 on 2023-05-05 19:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tmap', '0006_remove_centerlist_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispatchlist',
            name='mappingKey',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='dispatchlist',
            name='optionType',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='dispatchlist',
            name='orderList',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tmap.orderlist'),
        ),
        migrations.AddField(
            model_name='dispatchlist',
            name='startTime',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='dispatchlist',
            name='vehicleList',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tmap.vehiclelist'),
        ),
        migrations.AddField(
            model_name='orderlist',
            name='deliveryVolume',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orderlist',
            name='deliveryWeight',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orderlist',
            name='geo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tmap.geoinformation'),
        ),
        migrations.AddField(
            model_name='orderlist',
            name='orderId',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orderlist',
            name='orderName',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orderlist',
            name='serviceTime',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='orderlist',
            name='updateDate',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='orderlist',
            name='vehicleType',
            field=models.CharField(default='2', max_length=100),
        ),
        migrations.AddField(
            model_name='orderlist',
            name='zoneCode',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vehiclelist',
            name='inputYn',
            field=models.CharField(default='1', max_length=10),
        ),
        migrations.AddField(
            model_name='vehiclelist',
            name='skillPer',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='vehiclelist',
            name='vehicleId',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vehiclelist',
            name='vehicleName',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vehiclelist',
            name='vehicleType',
            field=models.CharField(default='2', max_length=100),
        ),
        migrations.AddField(
            model_name='vehiclelist',
            name='volume',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='vehiclelist',
            name='weight',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='vehiclelist',
            name='zoneCode',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='zonlist',
            name='code',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='zonlist',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='DispatchListResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('routeList', models.CharField(max_length=1000)),
                ('orderList', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tmap.orderlist')),
                ('vehicleList', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tmap.vehiclelist')),
            ],
        ),
    ]
