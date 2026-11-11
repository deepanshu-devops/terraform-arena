"""Google OAuth 2.0 helpers.

The app deliberately keeps this dependency surface small: a signed-cookie
session (Starlette) carries the local user id, while Google is used only for
the initial identity proof.  When the Google client credentials are absent the
app falls back to the historical local profile so offline development keeps
working.
"""
from __future__ import annotations

import base64
import hashlib
import os
import secrets
from typing import Any
from urllib.parse import urlencode

AUTHORIZE_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
OAUTH_SCOPE = "openid email profile"

SESSION_COOKIE = "arena_session"
_SESSION_SECRET = os.getenv("ARENA_SECRET_KEY", "").strip() or secrets.token_hex(32)


class AuthError(RuntimeError):
    """Raised when an OAuth callback cannot be trusted."""


def _env(name: str) -> str:
    return os.getenv(name, "").strip()


def client_id() -> str:
    return _env("GOOGLE_CLIENT_ID")


def client_secret() -> str:
    return _env("GOOGLE_CLIENT_SECRET")


def auth_enabled() -> bool:
    """True when the deployment has enough configuration to use Google."""
    return bool(client_id() and client_secret())


def session_secret() -> str:
    return _SESSION_SECRET


def https_only() -> bool:
    configured = _env("ARENA_HTTPS_ONLY").lower()
    if configured:
        return configured not in {"0", "false", "no", "off"}
    return _env("GOOGLE_REDIRECT_URI").startswith("https://")


def redirect_uri(request: Any) -> str:
    configured = _env("GOOGLE_REDIRECT_URI")
    if configured:
        return configured
    public = _env("ARENA_PUBLIC_URL").rstrip("/")
    if public:
        return f"{public}/auth/google/callback"
    # request.url_for honours the host header and is the sensible local
    # fallback.  Production should still set GOOGLE_REDIRECT_URI explicitly.
    return str(request.url_for("google_callback"))


def _pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def new_login_state() -> tuple[str, str, str]:
    """Return (state, PKCE verifier, nonce) for one OAuth round trip."""
    state = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(64)
    nonce = secrets.token_urlsafe(32)
    return state, verifier, nonce


def authorization_url(
    *,
    state: str,
    code_verifier: str,
    nonce: str,
    redirect: str,
    prompt: str = "select_account",
) -> str:
    params = {
        "client_id": client_id(),
        "redirect_uri": redirect,
        "response_type": "code",
        "scope": OAUTH_SCOPE,
        "state": state,
        "nonce": nonce,
        "code_challenge": _pkce_challenge(code_verifier),
        "code_challenge_method": "S256",
        "access_type": "online",
        "include_granted_scopes": "true",
        "prompt": prompt,
    }
    return AUTHORIZE_ENDPOINT + "?" + urlencode(params)


def _verify_id_token(token: str) -> dict[str, Any]:
    try:
        from google.auth.transport.requests import Request as GoogleRequest
        from google.oauth2 import id_token as google_id_token
    except ImportError as exc:  # pragma: no cover - dependency guard
        raise AuthError(
            "Google sign-in needs google-auth. Install requirements.txt and redeploy."
        ) from exc

    try:
        info = google_id_token.verify_oauth2_token(
            token,
            GoogleRequest(),
            client_id(),
        )
    except Exception as exc:  # google-auth raises several exception types
        raise AuthError(f"Google ID token verification failed: {exc}") from exc

    if info.get("iss") not in ("accounts.google.com", "https://accounts.google.com"):
        raise AuthError("Unexpected Google token issuer.")
    if not info.get("email_verified", False):
        raise AuthError("Google account email is not verified.")
    if not info.get("sub"):
        raise AuthError("Google account is missing a stable subject id.")
    return info


def exchange_code(
    *,
    code: str,
    code_verifier: str | None,
    redirect: str,
    nonce: str | None,
) -> dict[str, Any]:
    """Exchange an authorization code and return verified Google claims."""
    if not auth_enabled():
        raise AuthError("Google sign-in is not configured on this deployment.")

    try:
        import requests
    except ImportError as exc:  # pragma: no cover - dependency guard
        raise AuthError("Google sign-in needs requests. Install requirements.txt.") from exc

    data = {
        "code": code,
        "client_id": client_id(),
        "client_secret": client_secret(),
        "redirect_uri": redirect,
        "grant_type": "authorization_code",
    }
    if code_verifier:
        data["code_verifier"] = code_verifier

    try:
        response = requests.post(TOKEN_ENDPOINT, data=data, timeout=20)
    except requests.RequestException as exc:
        raise AuthError(f"Could not reach Google's token endpoint: {exc}") from exc

    if response.status_code >= 400:
        detail = response.text[:300]
        raise AuthError(f"Google token exchange failed ({response.status_code}): {detail}")

    try:
        payload = response.json()
    except ValueError as exc:
        raise AuthError("Google token endpoint returned an invalid response.") from exc

    token = payload.get("id_token")
    if not token:
        raise AuthError("Google did not return an ID token.")

    info = _verify_id_token(token)
    if nonce and info.get("nonce") != nonce:
        raise AuthError("OAuth nonce mismatch.")
    return info
