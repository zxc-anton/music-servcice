from src.apps.stream_servic.dependency import s3_client
import asyncio


class StreamMusic:
    def __init__(self, s3_client: s3_client) -> None:
        self.s3_client = s3_client

    async def get_music(self, key: str, start: int, end: int | None = None):
        range_header = f"bytes={start}-{end}" if end else f"bytes={start}-"
        async with self.s3_client.get_client() as client:
            response = await asyncio.to_thread(client.get_object(
                Key=key,
                Range=range_header,
                Bucket=self.s3_client.bucket_name
            ))
        try:
            stream = response["Body"]
            while True:
                chank = asyncio.to_thread(stream.read, 8192)
                if not chank:
                    break
                yield chank
        except:
            print(response[""])

    async def get_music_options(self, filename: str):
        async with self.s3_client.get_client() as client:
            file_options = await client.head_object(Key=filename, Bucket=self.s3_client.bucket_name)
        return {
            "Content-Length": str(file_options["ContentLength"]),
            "Content-Type": file_options.get("ContentType", "audio/mpeg"),
        }