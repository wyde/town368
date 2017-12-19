from django.db import models

# Create your models here.
class Report(models.Model):
    rid = models.AutoField(primary_key=True)
    station_sid = models.IntegerField(blank=True, null=True)
    update_t = models.DateTimeField(blank=True, null=True)
    record_t = models.DateTimeField(blank=True, null=True)
    weekday = models.CharField(max_length=3, blank=True, null=True)
    wx = models.CharField(max_length=32, blank=True, null=True)
    t = models.IntegerField(blank=True, null=True)
    at = models.IntegerField(blank=True, null=True)
    beaufort = models.CharField(max_length=16, blank=True, null=True)
    wind_dir = models.CharField(max_length=3, blank=True, null=True)
    rh = models.CharField(max_length=4, blank=True, null=True)
    pop = models.CharField(max_length=4, blank=True, null=True)
    ci = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report'
        verbose_name = "Report"
        verbose_name_plural = "Reports"


class Station(models.Model):
    sid = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=8, blank=True, null=True)
    district = models.CharField(unique=True, max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'station'
        verbose_name = "Station"
        verbose_name_plural = "Stations"
