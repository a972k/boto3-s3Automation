# Example usage of S3 file operations using variables from variables.py

from variables import AWS_REGION, BUCKET_NAME, LOCAL_FILE_PATH, OBJECT_NAME
from file_func import upload_file_if_not_exists, list_files_in_bucket, delete_file_from_bucket

if __name__ == "__main__":
    # Upload a file if it does not already exist
    upload_file_if_not_exists(BUCKET_NAME, LOCAL_FILE_PATH, OBJECT_NAME, AWS_REGION)

    # List all files in the bucket
    list_files_in_bucket(BUCKET_NAME, AWS_REGION)

    # Example: Delete a file (uncomment and set OBJECT_NAME to use)
    # delete_file_from_bucket(BUCKET_NAME, 'file_to_delete.txt', AWS_REGION)
