from aiobotocore.session import get_session
from settings.setting import settings
from contextlib import asynccontextmanager


class S3_client:
    def __init__(self) -> None:
        self._config = {
            "aws_access_key_id": settings.s3_client.s3_access_key,
            "aws_secret_access_key": settings.s3_client.s3_secret_key.get_secret_value(),
            "endpoint_url": settings.s3_client.s3_endpoint_url
        }
        self._session = get_session()
        self.bucket_name = settings.s3_client.s3_bucket_name
    
    @asynccontextmanager
    async def get_client(self):
        async with self._session.create_client(**self._config) as client:
            try:
                yield client
            finally:
                await client.close()