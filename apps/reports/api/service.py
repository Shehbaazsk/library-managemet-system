
import os
from pathlib import Path

from django.conf import settings
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response

from apps.reports.tasks import generate_report


class ReportService:
    @staticmethod
    def report_generation():
        """
        Celery task for generating a new report.
        """
        task = generate_report.delay()
        return Response(
            {"message": "Report generation has been triggered.",
                "task_id": task.id},
            status=status.HTTP_202_ACCEPTED
        )

    @staticmethod
    def get_latest_report():
        """
        Retrieve the latest generated report.
        """
        reports_dir = Path(settings.BASE_DIR) / "reports"
        if not reports_dir.exists():
            raise FileNotFoundError("No reports directory found.")

        report_files = sorted(
            [f for f in os.listdir(reports_dir) if f.startswith(
                "report_") and f.endswith(".json")],
            reverse=True
        )

        if not report_files:
            raise FileNotFoundError("No reports found.")

        latest_report_file = os.path.join(reports_dir, report_files[0])

        return FileResponse(
            open(latest_report_file, 'rb'),
            as_attachment=True,
            filename=os.path.basename(latest_report_file)
        )
