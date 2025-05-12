# eventify/storage.py

from storages.backends.s3boto3 import S3Boto3Storage
from dotenv import load_dotenv
import os

load_dotenv()

class MediaStorage(S3Boto3Storage):
    bucket_name = os.getenv('MINIO_BUCKET_NAME', 'media')

    def url(self, name):
        url = super().url(name)
        return url.replace("https://minio:9000/", "")  # 💥 хак, но работает
