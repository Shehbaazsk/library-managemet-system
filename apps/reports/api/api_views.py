
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.reports.api.service import ReportService


class GenerateAndDownloadReportAPIView(APIView):
    """
    API  to trigger report generation in the background and download report.
    """

    # permission_classes = [AllowAny]

    def post(self, request):
        try:
            return ReportService.report_generation()
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        try:
            return ReportService.get_latest_report()
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
