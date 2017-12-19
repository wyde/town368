from django.shortcuts import render

# Create your views here.
from ntucourt.models import Report, Station
from ntucourt.serializers import ReportSerializer, StationSerializer
from rest_framework import viewsets
#from rest_framework import generics


class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    #queryset = Report.objects.all()
    serializer_class = ReportSerializer
    def get_queryset(self):
        queryset = Report.objects.all()
        station_sid = self.request.query_params.get('station_sid', None)
        record_t = self.request.query_params.get('record_t', None)
        if record_t is not None and station_sid is not None:
            queryset = queryset.filter(station_sid=station_sid, record_t=record_t)
        elif record_t is not None:
            queryset = queryset.filter(record_t=record_t)
        elif station_sid is not None:
            queryset = queryset.filter(station_sid=station_sid)
        return queryset

class StationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    def get_queryset(self):
        queryset = Station.objects.all()
        city = self.request.query_params.get('city', None)
        district = self.request.query_params.get('district', None)
        if city is not None and district is not None:
            queryset = queryset.filter(city=city, district=district)
        elif city is not None:
            queryset = queryset.filter(city=city)
        elif district is not None:
            queryset = queryset.filter(district=district)
        return queryset

