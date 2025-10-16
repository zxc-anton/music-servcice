from src.apps.stream_servic.main import router
from fastapi.responses import ORJSONResponse, StreamingResponse
from src.schemas import ID_Field
from fastapi import Request
from src.apps.stream_servic.dependency import streamer


@router.get("/{ID}", status_code=206)
async def stream_song(ID: int, request: Request, streamer: streamer): 
    range_header = request.headers.get("Range")
    _, range_opts = range_header.split("=")
    start_end = range_opts.split("-")
    start = int(start_end[0]) if start_end[0] else 0
    end = int(start_end[1]) if start_end[1] else None
    return StreamingResponse(streamer.get_music(key=f"{ID}.mp3", start=start, end=end),
                             status_code=206
                             )

@router.head("/{ID}")
async def options(ID: int, streamer: streamer): 
    options = await streamer.get_music_options(filename=f"{ID}.mp3")
    return ORJSONResponse(
        status_code=200,
        content="",
        headers={
            **options,
            "Accept-Ranges": "bytes"
        }
    )