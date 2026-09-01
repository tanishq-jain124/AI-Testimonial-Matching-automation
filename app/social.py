from urllib.parse import urlparse
import httpx
from bs4 import BeautifulSoup
from app.config import settings

def valid_url(url: str) -> bool:
    try:
        p = urlparse(url)
        return p.scheme in {"http", "https"} and bool(p.netloc)
    except Exception:
        return False

async def collect_public_social_data(social_id: str | None) -> dict:
    # Conservative collector: no login, CAPTCHA solving, private-content access,
    # anti-bot bypassing, or other access-control circumvention.
    if not social_id or not valid_url(social_id):
        return {"status": "unavailable", "source": social_id or "", "text": ""}

    try:
        async with httpx.AsyncClient(
            timeout=8,
            follow_redirects=True,
            headers={"User-Agent": "AI-Yearbook/1.0"}
        ) as client:
            response = await client.get(social_id)

        if response.status_code >= 400:
            return {"status": "blocked_or_unavailable", "source": social_id, "text": ""}

        if "text/html" not in response.headers.get("content-type", ""):
            return {"status": "unsupported_content", "source": social_id, "text": ""}

        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = " ".join(soup.stripped_strings)[:settings.MAX_SOCIAL_TEXT]
        return {"status": "ok", "source": social_id, "text": text}
    except Exception:
        return {"status": "error", "source": social_id, "text": ""}
