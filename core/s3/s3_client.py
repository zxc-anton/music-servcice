from settings.setting import settings
from aiobotocore.session import get_session
from contextlib import asynccontextmanager

class S3_client:
    def __init__(self)-> None:
        self.config = {
            "aws_access_key_id": settings.s3_client.s3_access_key,
            "aws_secret_access_key": settings.s3_client.s3_secret_key.get_secret_value(),
            "endpoint_url": settings.s3_client.s3_endpoint_url,
            "region_name": settings.s3_client.s3_region_name
        }
        self.bucket_name = settings.s3_client.s3_bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client  