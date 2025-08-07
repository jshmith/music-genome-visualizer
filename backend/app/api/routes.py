from fastapi import APIRouter, Response, Request, status, HTTPException
from fastapi.responses import JSONResponse
from app.spotify_client import get_spotify_auth_url, exchange_code_for_token

# APIRouter allows us to modularly organize endpoints
router = APIRouter()

## --------------- Endpoints ---------------

# Root
@router.get("/")
async def root():
    return {"message": "Music Taste Genome Backend is running"}

# Spotify authorization
@router.get("/auth/login")
async def login():
    auth_url = get_spotify_auth_url()
    # Redirect user to Spotify's OAuth consent screen
    return Response(status_code=status.HTTP_302_FOUND, headers={"Location": auth_url})

# Authorizatrion callback - exchange for tokens
@router.get("/auth/callback")
async def auth_callback(request: Request):
    code = request.query_params.get("code")
    error = request.query_params.get("error")

    if error:
        raise HTTPException(status_code=400, detail=f"Spotify auth error: {error}")

    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    try:
        token_data = exchange_code_for_token(code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Token exchange failed: {str(e)}")

    # For now, just return the tokens as JSON to verify it works
    return JSONResponse(content=token_data)