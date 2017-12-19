from rest_framework import serializers
from ntucourt.models import Station, Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__' 

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__' 

