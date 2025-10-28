from src.apps.stream_servic.main import router
from fastapi.responses import ORJSONResponse, StreamingResponse, Response
from src.schemas import ID_Field
from fastapi import HTTPException, Request
from src.apps.stream_servic.dependency import streamer
import re


@router.get("/{file_id}")
async def stream_music(file_id: int, request: Request, stream_service: streamer):
    try:
        # Получаем информацию о файле
        file_options = await stream_service.get_music_options(str(file_id))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="File not found")
    
    file_size = int(file_options["Content-Length"])
    content_type = file_options["Content-Type"]
    
    # Обрабатываем Range заголовок
    range_header = request.headers.get("Range")
    start = 0
    end = file_size - 1
    status_code = 200
    
    if range_header:
        match = re.match(r"bytes=(\d+)-(\d*)", range_header)
        if match:
            start = int(match.group(1))
            end = int(match.group(2)) if match.group(2) else file_size - 1
            status_code = 206  # Partial Content
    
    # Убедимся, что end не превышает размер файла
    end = min(end, file_size - 1)
    chunk_size = end - start + 1
    
    # Заголовки для аудиоплеера
    headers = {
        "Accept-Ranges": "bytes",
        "Content-Length": str(chunk_size),
        "Content-Type": content_type,
        "Content-Disposition": "inline"
    }
    
    if range_header:
        headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"
    
    return StreamingResponse(
        content=stream_service.get_music(f"{file_id}", start, end),
        status_code=status_code,
        headers=headers,
        media_type=content_type
    )

@router.options("/{file_id}")
async def options_music():
    """Для CORS preflight requests"""
    return Response(headers={
        "Allow": "GET, HEAD, OPTIONS",
        "Accept-Ranges": "bytes",
    })