from src.apps.stream_servic.dependency import s3_client
from aiobotocore.response import StreamingBody


class StreamMusic:
    def __init__(self, s3_client: s3_client) -> None:
        self.s3_client = s3_client

    async def get_music(self, key: str, start: int, end: int | None = None):
        range_header = f"bytes={start}-{end}" if end else f"bytes={start}-"
        
        async with self.s3_client.get_client() as client:
            response = await client.get_object(
                Key=key,
                Range=range_header,
                Bucket=self.s3_client.bucket_name
            )
            
            try:
                stream: StreamingBody = response["Body"]
                async with stream:
                    while chunk := await stream.read(8192):  # Исправлен размер чанка
                        yield chunk
            except Exception as e:
                print(f"Stream reading error: {e}")
            finally:
                if not response.get("Body")._closed:
                    await response["Body"].close()

    async def get_music_options(self, filename: str):
        async with self.s3_client.get_client() as client:
            file_options = await client.head_object(Key=filename, Bucket=self.s3_client.bucket_name)
        
        return {
            "Content-Length": str(file_options["ContentLength"]),
            "Content-Type": file_options.get("ContentType", "audio/mpeg"),
            "Accept-Ranges": "bytes",
            "Content-Range": f"bytes 0-{file_options['ContentLength']-1}/{file_options['ContentLength']}",
        }
