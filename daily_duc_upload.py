import os
import boto3
from botocore.exceptions import ClientError
from variables import AWS_REGION, BUCKET2_NAME  # Backup bucket name and region

def get_s3_client():
    """Create and return an S3 client using the AWS_REGION variable."""
    return boto3.client("s3", region_name=AWS_REGION)

def ensure_bucket_exists(bucket_name, region):
    """Create the bucket if it does not exist."""
    s3 = get_s3_client()
    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
            print(f"Bucket '{bucket_name}' created.")
        else:
            raise

def list_existing_objects(bucket_name):
    """Return a set of all file names (keys) currently stored in the specified S3 bucket."""
    s3 = get_s3_client()
    existing = set()
    paginator = s3.get_paginator("list_objects_v2")
    try:
        for page in paginator.paginate(Bucket=bucket_name):
            for obj in page.get("Contents", []):
                existing.add(obj["Key"])
    except ClientError:
        raise
    return existing

def upload_files_with_skip(bucket_name, folder_path):
    """
    Upload every file from the local folder to the specified S3 bucket,
    but skip files that already exist in the bucket.
    """
    s3 = get_s3_client()
    print("Starting upload of daily documents…")

    try:
        existing = list_existing_objects(bucket_name)
    except ClientError:
        existing = set()  # Assume bucket is empty if we can't list it

    for entry in os.listdir(folder_path):
        full_path = os.path.join(folder_path, entry)
        if not os.path.isfile(full_path):
            continue
        key = entry
        if key in existing:
            print(f"File already exists: {key}")
        else:
            try:
                s3.upload_file(full_path, bucket_name, key)
                print(f"Uploaded: {key}")
            except ClientError as e:
                print(f"Failed to upload {key}: {e}")

if __name__ == "__main__":
    folder = "daily_documents"
    if not os.path.isdir(folder):
        print(f"Folder '{folder}' does not exist. Please create it and add files to upload.")
    else:
        ensure_bucket_exists(BUCKET2_NAME, AWS_REGION)
        upload_files_with_skip(BUCKET2_NAME, folder)
