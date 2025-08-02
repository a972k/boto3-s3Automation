
# Import boto3 for AWS SDK and ClientError for error handling
import boto3
from botocore.exceptions import ClientError
from variables import AWS_REGION

# Function to upload a file to S3 if it does not already exist
def upload_file_if_not_exists(BUCKET_NAME, file_path, object_name=None, region=None):
    """
    Upload a file to an S3 bucket if it does not already exist.
    Returns a tuple: (status: bool, message: str)
    """
    if not object_name:
        import os
        object_name = os.path.basename(file_path)
    s3_client = boto3.client('s3', region_name=AWS_REGION) if region else boto3.client('s3')
    # Check if the object already exists
    try:
        s3_client.head_object(Bucket=BUCKET_NAME, Key=object_name)
        return False, f"File '{object_name}' already exists in bucket '{BUCKET_NAME}'. Upload skipped."
    except ClientError as e:
        if e.response['Error']['Code'] != '404':
            return False, f"Error checking file existence: {e}"
    # Upload the file
    try:
        s3_client.upload_file(file_path, BUCKET_NAME, object_name)
        return True, f"File '{object_name}' uploaded to bucket '{BUCKET_NAME}'."
    except ClientError as e:
        return False, f"Error uploading file: {e}"


# Function to list all files in a bucket
def list_files_in_bucket(BUCKET_NAME, region=None):
    """
    List all files in the specified S3 bucket.
    Returns a tuple: (list_of_files: list, message: str)
    """
    s3_client = boto3.client('s3', region_name=AWS_REGION) if region else boto3.client('s3')
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        if 'Contents' in response:
            files = [obj['Key'] for obj in response['Contents']]
            return files, f"Files in bucket '{BUCKET_NAME}': {files}"
        else:
            return [], f"Bucket '{BUCKET_NAME}' is empty."
    except ClientError as e:
        return [], f"Error listing files: {e}"


# Function to delete a file from a bucket
def delete_file_from_bucket(BUCKET_NAME, object_name, region=None):
    """
    Delete a file from the specified S3 bucket.
    Returns a tuple: (status: bool, message: str)
    """
    s3_client = boto3.client('s3', region_name=AWS_REGION) if region else boto3.client('s3')
    try:
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=object_name)
        return True, f"File '{object_name}' deleted from bucket '{BUCKET_NAME}'."
    except ClientError as e:
        return False, f"Error deleting file: {e}"
