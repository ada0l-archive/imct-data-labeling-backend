from boto3 import logging
from backend.core.localstack import get_s3_client


def shutdown_handler():
    print("shutdown")


def startup_handler():
    print("startup")


def create_bucket_for_images():
    try:
        client = get_s3_client()
        client.create_bucket(Bucket="images")
        logging.info("Image bucket created")
    except:
        logging.error("Image bucket not created")
