import boto3, os

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=os.getenv("AWS_REGION"),
)


def upload_file_to_s3(file_path, bucket, key):
    s3.upload_file(file_path, bucket, key)
    return f"https://{bucket}.s3.amazonaws.com/{key}"