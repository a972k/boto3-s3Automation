import os
import boto3
from botocore.exceptions import ClientError
from variables import AWS_REGION, BUCKET2_NAME  # Backup bucket name and region

def get_s3_client():
    """
    Create and return an S3 client using the AWS_REGION variable.
    Assumes AWS credentials are already configured in the environment.
    """
    return boto3.client("s3", region_name=AWS_REGION)

def list_existing_objects(bucket_name):
    """
    Get a set of all file names (keys) currently stored in the specified S3 bucket.

    Raises:
        ClientError: If the bucket doesn't exist or access is denied.
    """
    s3 = get_s3_client()
    existing = set()
    paginator = s3.get_paginator("list_objects_v2")
    # Go through all pages of the bucket's contents and collect object keys (file names)
    try:
        for page in paginator.paginate(Bucket=bucket_name):
            for obj in page.get("Contents", []):
                existing.add(obj["Key"])
    except ClientError:
        # Pass the error up to the caller (could be missing bucket or permissions)
        raise
    return existing

def upload_files_with_skip(bucket_name, folder_path):
    """
    Upload every file from the local folder to the specified S3 bucket,
    but skip files that already exist in the bucket.

    Prints:
      - "Starting upload of daily documents…" at the beginning.
      - "File already exists: [filename]" if the file is already in S3.
      - "Uploaded: [filename]" after a successful upload.
      - "Failed to upload [filename]: [error]" if an upload fails.
    """
    s3 = get_s3_client()
    print("Starting upload of daily documents…")

    # Try to get the list of existing files in the bucket.
    # If the bucket doesn't exist or can't be listed, act as if it's empty.
    try:
        existing = list_existing_objects(bucket_name)
    except ClientError:
        existing = set()  # Assume bucket is empty if we can't list it

    # Go through each file in the local folder
    for entry in os.listdir(folder_path):
        full_path = os.path.join(folder_path, entry)

        # Only process regular files (ignore directories, etc.)
        if not os.path.isfile(full_path):
            continue

        key = entry  # Use the file name as the S3 object key

        if key in existing:
            # File is already in the bucket, skip uploading
            print(f"File already exists: {key}")
        else:
            # Upload the file to S3
            try:
                s3.upload_file(full_path, bucket_name, key)
                print(f"Uploaded: {key}")
            except ClientError as e:
                # Print an error message but continue with other files
                print(f"Failed to upload {key}: {e}")
