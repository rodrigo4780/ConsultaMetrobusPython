from django.db import models


class Alcaldia(models.Model):
    name = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class MetrobusData(models.Model):
    id_data = models.IntegerField(blank=True, null=True)
    id_alcaldia = models.ForeignKey(Alcaldia, on_delete=models.CASCADE, blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    vehicle_id = models.IntegerField(blank=True, null=True)
    vehicle_label = models.IntegerField(blank=True, null=True)
    vehicle_current_status = models.IntegerField(blank=True, null=True)
    position_latitude = models.FloatField(blank=True, null=True)
    position_longitude = models.FloatField(blank=True, null=True)
    geographic_point = models.CharField(max_length=300, blank=True, null=True)
    position_speed = models.IntegerField(blank=True, null=True)
    position_odometer = models.IntegerField(blank=True, null=True)
    trip_schedule_relationship = models.IntegerField(blank=True, null=True)
    trip_id = models.IntegerField(blank=True, null=True)
    trip_start_date = models.IntegerField(blank=True, null=True)
    trip_route_id = models.IntegerField(blank=True, null=True)
