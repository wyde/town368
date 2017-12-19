from django.conf.urls import url, include
from rest_framework import routers
from ntucourt.views import ReportViewSet, StationViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'v1.0/reports', ReportViewSet, base_name='report')
router.register(r'v1.0/stations', StationViewSet, base_name='station')

urlpatterns = router.urls
