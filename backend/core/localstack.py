import logging

import boto3

from backend.core.settings import settings


def get_s3_client():
    return boto3.client(
        "s3",
        region_name="us-east-1",
        endpoint_url=settings.localstack_url,
        aws_access_key_id=settings.localstack_access_key,
        aws_secret_access_key=settings.localstack_secret_key,
    )


async def upload_image(file_obj, obj_name=None):
    if obj_name is None:
        obj_name = file_obj
    try:
        client = get_s3_client()
        content = await file_obj.read()
        client.put_object(Body=content, Bucket="images", Key=f"{obj_name}")
    except Exception as e:
        logging.error(e)
        return False
    return True
