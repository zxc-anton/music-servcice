from src.apps.stream_servic.main import router
from fastapi.responses import ORJSONResponse


@router.get("/{ID}", status_code=206)
async def stream_song(ID: int): pass

@router.head("/{ID}")
async def options(ID: int): 
    return ORJSONResponse(
        status_code=200,
        content="",
        headers={
            "": ""
        }
    )