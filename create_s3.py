


# Import boto3 for AWS SDK and ClientError for error handling
import boto3
from botocore.exceptions import ClientError
import json
# filepath: c:\Users\rolle\OneDrive\Documents\GitHub\boto3+s3Automation\create_s3.py
from variables import BUCKET_NAME, BUCKET2_NAME, AWS_REGION

def create_bucket(bucket_name, region=None):
    """
    Create an S3 bucket in a specified region using boto3 client.
    If no region is specified, the default AWS region is used.
    After creation, applies a public policy for read, write, and delete.
    """
    try:
        # Create S3 client
        if region is None:
            s3_client = boto3.client('s3')
            # Create bucket with default region
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            # Specify region in bucket configuration
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

        # Wait until the bucket exists to ensure setup is complete
        waiter = s3_client.get_waiter('bucket_exists')
        print(f"Waiting for bucket '{bucket_name}' to be available...")
        waiter.wait(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created and is now available.")

        # Define a bucket policy granting public read, write, and delete permissions
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadWriteDelete",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": [
                        "s3:GetObject",
                        "s3:PutObject",
                        "s3:DeleteObject"
                    ],
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }

        # Convert the policy to a JSON string
        bucket_policy_str = json.dumps(bucket_policy)

        # Apply the bucket policy
        s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy_str)
        print(f"Public read/write/delete policy applied to bucket '{bucket_name}'.")
    except ClientError as e:
        # Print error if bucket creation fails
        print(f"Error: {e}")



# The create_bucket function is now modular and can be imported and used in other scripts.
# Example usage (uncomment to use as a script):
if __name__ == "__main__":
    # Create the main bucket
    create_bucket(BUCKET_NAME, AWS_REGION)
    # Create the backup bucket
    create_bucket(BUCKET2_NAME, AWS_REGION)