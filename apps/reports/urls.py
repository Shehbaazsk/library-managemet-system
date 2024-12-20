from django.urls import path

from apps.reports.api.api_views import GenerateAndDownloadReportAPIView

urlpatterns = [
    path('reports/', GenerateAndDownloadReportAPIView.as_view(),
         name='generate-download-report'),
]
