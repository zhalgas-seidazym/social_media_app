# Muryn Social Media App

This is a Social Media App built with Django, Docker, NGINX, PostgreSQL, and MinIO for media storage.

## 🚀 Prerequisites

* Python 3.10+
* Docker and Docker Compose installed
* PostgreSQL
* MinIO (for media storage)

---

## ✅ Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/zhalgas-seidazym/social_media_app.git
cd social_media_app
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate   # For Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Setup MinIO (for Media Storage)

* Go to MinIO Web Interface: `http://localhost:9000`
* Login with your credentials.
* Create a new bucket named `media`.
* Set the bucket to **public** for access.

### 7. Start the Application with Docker Compose

```bash
docker-compose up --build -d
```

### 8. Access the Application

* Frontend: `http://localhost`
* Admin Panel: `http://localhost/admin`
* API: `http://localhost/api`

---

## ✅ Environment Variables (.env)

Make sure you have a `.env` file with the following variables:

```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_URL=postgres://your_db_user:your_db_password@db:5432/your_database_name
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=media
```

---

## ✅ Troubleshooting

* If migrations do not apply correctly, make sure the database is running.
* If MinIO does not allow public access, check the bucket settings.
* If NGINX does not serve your app, make sure your NGINX config is correct.

---

## ✅ License

This project is licensed under the MIT License.
