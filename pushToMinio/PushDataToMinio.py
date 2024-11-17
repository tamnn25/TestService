import json
from minio import Minio
from minio.error import S3Error

# Load credentials from the downloaded JSON file
with open('credentials.json', 'r') as f:
    credentials = json.load(f)

# Extract the MinIO server URL, access key, and secret key from the JSON
# minio_url = credentials['url']  # URL of your MinIO instance
minio_url = "localhost:9000"
access_key = credentials['accessKey']  # Access key from the file
secret_key = credentials['secretKey']  # Secret key from the file

# Set the name of the bucket and the file to upload
bucket_name = "finviet"  # Replace with your MinIO bucket name
file_path = "docker-compose.yml"  # Replace with the path to the file you want to upload
object_name = "file-name-on-minio11.json"  # Replace with the name you want for the object in MinIO

# Initialize the MinIO client with the extracted credentials
client = Minio(
    minio_url,
    access_key=access_key,
    secret_key=secret_key,
    secure=False  # Set to True if you're using HTTPS
)

# Check if the bucket exists, and create it if it does not
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)

# Upload the file to the specified bucket
try:
    client.fput_object(bucket_name, object_name, file_path)
    print(f"File '{file_path}' uploaded successfully to '{bucket_name}/{object_name}'")
except S3Error as err:
    print(f"Error occurred: {err}")
