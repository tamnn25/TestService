import os
import json
from minio import Minio
from minio.error import S3Error

with open('credentials.json', 'r') as f:
    credentials = json.load(f)

# minio_url = credentials['url']  # URL of your MinIO instance
minio_url = "localhost:9000"

access_key = credentials['accessKey']  # Access key from the file
secret_key = credentials['secretKey']  # Secret key from the file

client = Minio(
    minio_url,
    access_key=access_key,
    secret_key=secret_key,
    secure=False  # Set to True if you're using HTTPS
)

# Set the bucket name and the local directory to upload
bucket_name = "finviet"  # Replace with your MinIO bucket name
folder_path = "/Users/tamnn/Documents/GitHub/TestService/pushdata"  # Replace with the local folder path you want to upload

# Ensure the bucket exists, and create it if necessary
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)

# Walk through the folder and upload each file
for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        object_name = os.path.relpath(file_path, folder_path)

        try:
            # Upload the file to MinIO
            client.fput_object(bucket_name, object_name, file_path)
            print(f"File '{file_path}' uploaded successfully as '{object_name}'")
        except S3Error as err:
            print(f"Error uploading {file_path}: {err}")
