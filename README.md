# Library Management System

A Django-based library management system with features for managing books, authors, borrow records, and generating reports with background tasks.

## Features

- **Book Management**: Add, list, and manage books.
- **Author Management**: Manage authors and associate them with books.
- **Borrow Records**: Track borrowed books and manage returns.
- **Reports**: Generate and download reports about authors, books, and borrowed books.
- **Background Tasks**: Reports are generated asynchronously using Celery.

---

## Technologies Used

- **Django**: Framework for backend APIs.
- **Celery**: Background task processing.
- **Redis**: Task queue broker for Celery.
- **PostgreSQL**: Database for storing data.
- **DRF (Django Rest Framework)**: For building RESTful APIs.

---

## Setup Instructions

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/Shehbaazsk/library-managemet-system.git
cd library-managemet-system
```
### 2. Create a Virtual Environment
Set up a virtual environment to keep your dependencies isolated:

```bash
Copy code
python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
```
### 3. Install Dependencies
Install the required Python packages:

```bash
Copy code
pip install -r requirements.txt
```
### 4. Configure PostgreSQL
Install PostgreSQL (if not installed).
Create a new PostgreSQL database and user.
Update the DATABASES settings in settings.py with your database credentials.
### 5. Run Migrations
Apply database migrations:
```bash
Copy code
python manage.py makemigrations
python manage.py migrate
```
### 6. Install Redis
Follow the official Redis [installation guide](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/) to install and configure Redis for task processing.

### 7. Create a Superuser (Optional)
To create a superuser for accessing the Django Admin panel:
```bash
Copy code
python manage.py createsuperuser
```
### 8. Start Django Server
Run the development server:

```bash
Copy code
python manage.py runserver
```
### 9. Start Celery Worker
Start the Celery worker to process background tasks:

```bash
Copy code
celery -A library_managemet_system worker --loglevel=info
```
### 10. Trigger Background Task (Generate Report)
* POST /reports/: Trigger the report generation in the background using Celery.
* GET /reports/: Download the latest generated report.
### API Endpoints
#### Books
* GET /api/books/: List all books.
* POST /api/books/: Add a new book.
#### Authors
* GET /api/authors/: List all authors.
* POST /api/authors/: Add a new author.
#### Borrow Records
* GET /api/borrow/: List all borrow records.
* POST /api/borrow/: Create a new borrow record (reduces the available copies of a book by 1).
* PUT /api/borrow/<id>/return/: Mark a book as returned (sets the return date and increases available copies by 1).
#### Reports
* POST /reports/: Trigger report generation (in the background).
* GET /reports/: Download the latest generated report (as a JSON file).
