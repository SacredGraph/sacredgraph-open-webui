import logging
import os
import time
from typing import Dict, Optional, Tuple

import httpx
from dotenv import load_dotenv
from fastapi import Cookie, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from jose import JWTError, jwt

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
PORT = int(os.getenv("PROXY_PORT", "3000"))
OUTSETA_DOMAIN = os.getenv("OUTSETA_DOMAIN")
JWKS_URL = f"https://{OUTSETA_DOMAIN}/.well-known/jwks"
FRONTEND_URL = os.getenv("PROXY_FRONTEND_URL", "http://localhost:5173")
TARGET_URL = os.getenv("PROXY_TARGET", "http://localhost:8081")

# JWKS cache configuration
JWKS_CACHE_TTL = 3600  # Cache JWKS for 1 hour
_jwks_cache: Dict[str, Tuple[dict, float]] = (
    {}
)  # Cache storage: {url: (jwks, expiration_time)}

# HTTP client for making requests
http_client = httpx.AsyncClient(base_url=TARGET_URL)


async def get_jwks() -> dict:
    """Get JWKS from cache or fetch from server if cache is expired."""
    current_time = time.time()

    # Check if we have a valid cached JWKS
    if JWKS_URL in _jwks_cache:
        jwks, expiration_time = _jwks_cache[JWKS_URL]
        if current_time < expiration_time:
            logger.info("[PROXY] Using cached JWKS")
            return jwks

    # Fetch fresh JWKS
    logger.info("[PROXY] Fetching fresh JWKS")
    async with httpx.AsyncClient() as client:
        jwks_response = await client.get(JWKS_URL)
        jwks = jwks_response.json()

    # Update cache
    _jwks_cache[JWKS_URL] = (jwks, current_time + JWKS_CACHE_TTL)
    return jwks


async def verify_jwt(token: str) -> Optional[dict]:
    """Verify JWT token and return payload if valid."""
    try:
        # Get JWKS from cache or fetch if needed
        jwks = await get_jwks()

        # Verify token
        payload = jwt.decode(
            token, jwks, algorithms=["RS256"], options={"verify_aud": False}
        )
        return payload
    except JWTError as e:
        logger.error(f"JWT verification failed: {e}")
        return None


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": True}


@app.api_route(
    "/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
)
async def proxy_request(
    request: Request,
    path: str,
    access_token: Optional[str] = None,
    outseta_token: Optional[str] = Cookie(None, alias="Outseta.nocode.accessToken"),
):
    """Main proxy endpoint that handles authentication and request forwarding."""
    # Handle access token in query params
    if access_token:
        response = RedirectResponse(url=FRONTEND_URL)
        response.set_cookie(
            key="Outseta.nocode.accessToken",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        return response

    # Verify JWT token
    headers = dict(request.headers)
    if outseta_token:
        logger.info(f"[PROXY] token: {outseta_token}")
        payload = await verify_jwt(outseta_token)

        if payload:
            logger.info(f"[PROXY] payload: {payload}")
            headers["X-User-Id"] = payload.get("outseta:accountUid", "")
            headers["X-User-Email"] = payload.get("email", "")
            headers["X-User-Name"] = (
                payload.get("name", "") or payload.get("email", "")
            ).strip()
            logger.info(f"[PROXY] headers: {headers}")

    # Forward the request to the target
    target_path = request.url.path
    if request.url.query:
        target_path += f"?{request.url.query}"

    try:
        response = await http_client.request(
            method=request.method,
            url=target_path,
            headers=headers,
            content=await request.body(),
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
    except Exception as e:
        logger.error(f"Error forwarding request: {e}")
        raise HTTPException(status_code=500, detail="Error forwarding request")
