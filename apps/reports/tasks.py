import json
import os
from datetime import datetime
from pathlib import Path

from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now

from apps.books.models import Book
from apps.borrow.models import BorrowRecord
from apps.users.models import Author

REPORTS_DIR = Path(settings.BASE_DIR) / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


@shared_task
def generate_report():
    """
    Generate a report including:
    - Total number of authors.
    - Total number of books.
    - Total books currently borrowed.
    """
    print("INSIDE GENERATE REPORT CELERY")
    total_authors = Author.objects.filter(user__is_delete=False).count()
    total_books = Book.objects.filter(is_delete=False).count()
    total_borrowed_books = BorrowRecord.objects.filter(
        return_date__isnull=True, is_delete=False).count()

    report_data = {
        "total_authors": total_authors,
        "total_books": total_books,
        "total_borrowed_books": total_borrowed_books,
    }

    filename = f"report_{now().strftime('%Y%m%d')}.json"
    filepath = REPORTS_DIR / filename

    with open(filepath, 'w') as report_file:
        json.dump(report_data, report_file, indent=4)

    return str(filename)
