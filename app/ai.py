import json
import re
import httpx
from difflib import SequenceMatcher
from app.config import settings

def extract_signals(text: str) -> dict:
    text = text or ""
    lowered = text.lower()
    keywords = {
        "technology": ["technology", "coding", "developer", "software", "ai", "python"],
        "travel": ["travel", "trip", "vacation", "trek", "hiking"],
        "sports": ["football", "cricket", "basketball", "sports", "gym"],
        "music": ["music", "guitar", "song", "concert"],
        "photography": ["photography", "camera", "photos", "photograph"],
        "food": ["food", "cooking", "recipe", "restaurant"],
        "academics": ["study", "college", "university", "research", "exam"],
    }
    topics = [topic for topic, words in keywords.items() if any(w in lowered for w in words)]

    style = []
    if any(x in lowered for x in ["haha", "lol", "😂", "funny", "joke"]):
        style.append("humorous/casual signals")
    if any(x in lowered for x in ["thank you", "thanks", "helped", "support"]):
        style.append("supportive/grateful communication signals")

    return {"recurring_topics": topics, "communication_signals": style}

def build_context(target, chats, social_data):
    social_text = (social_data or {}).get("text", "")
    return {
        "target": {
            "user_id": target.user_id,
            "full_name": target.full_name,
            "batch": target.batch,
        },
        "observable_social_signals": extract_signals(social_text),
        "public_social_text": social_text,
        "relevant_chat_context": [c.message for c in chats],
    }

async def generate_testimonial(context: dict, author_name: str, avoid_texts: list[str]) -> str:
    # ✅ Check if Groq API key is configured
    if not settings.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not configured. Please add it to .env file.")

    prompt = f'''
Write a natural yearbook testimonial.

Author: {author_name}
Target: {context["target"]["full_name"]}
Batch: {context["target"].get("batch")}

Observable non-sensitive signals:
{json.dumps(context["observable_social_signals"], ensure_ascii=False)}

Relevant permitted conversation context:
{json.dumps(context["relevant_chat_context"], ensure_ascii=False)}

Available public/authorized social text:
{context["public_social_text"][:settings.MAX_SOCIAL_TEXT]}

Existing testimonials that must not be copied:
{json.dumps(avoid_texts, ensure_ascii=False)}

Rules:
- Write about the target person.
- Sound like a real friend/classmate.
- Be warm, specific and natural.
- Use only information supported by the supplied context.
- Do not invent facts, achievements, events, relationships or hobbies.
- Do not infer sensitive personal attributes.
- Do not mention AI.
- Do not copy or lightly rewrite existing testimonials.
- Use a distinct angle and wording.
- Return only the testimonial, with no title or quotation marks.
- Approximately 60-120 words.
'''

    # 🔄 Groq API Call (OpenAI-compatible)
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    payload = {
        "model": settings.GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are an AI assistant that writes warm, personalized yearbook testimonials."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.9,
        "max_tokens": 300,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
    }

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(url, headers=headers, json=payload)
        
        # ✅ Better error handling
        if response.status_code != 200:
            error_detail = response.text
            try:
                error_json = response.json()
                error_detail = error_json.get("error", {}).get("message", error_detail)
            except:
                pass
            raise RuntimeError(f"Groq API error (status {response.status_code}): {error_detail}")
        
        data = response.json()

    try:
        # ✅ Groq returns OpenAI-compatible format
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected Groq response: {str(e)}")

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()

def highest_similarity(candidate: str, existing: list[str]) -> float:
    return max((similarity(candidate, x) for x in existing), default=0.0)