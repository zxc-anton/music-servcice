from core.s3.s3_client import S3_client
from fastapi import Depends
from typing import Annotated

s3_client = Annotated[S3_client, Depends(S3_client)]

from src.apps.stream_servic.streamer import StreamMusic
streamer = Annotated[StreamMusic, Depends(StreamMusic)]