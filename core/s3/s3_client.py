from aiobotocore.session import get_session
from settings.setting import settings
from contextlib import asynccontextmanager


class S3_client:
    def __init__(self,
                 aws_access_key_id: str = settings.s3_client.s3_access_key,
                 aws_secret_access_key: str = settings.s3_client.s3_secret_key.get_secret_value(),
                 endpoint_url: str = settings.s3_client.s3_endpoint_url,
                 bucket_name: str = settings.s3_client.s3_bucket_name
                 ) -> None:
        self._config = {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "endpoint_url": endpoint_url,
            "service_name": "s3"
        }
        self._session = get_session()
        self.bucket_name = bucket_name
    
    @asynccontextmanager
    async def get_client(self):
        async with self._session.create_client(**self._config) as client:
            try:
                yield client
            finally:
                await client.close()