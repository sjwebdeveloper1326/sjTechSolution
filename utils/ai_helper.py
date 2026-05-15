# from django.conf import settings
# from google import genai


# def _company_profile_text():
#     return (
#         f"Company Name: SG.Automix Tech\n"
#         f"Founded: {getattr(settings, 'COMPANY_START_YEAR', 2026)}\n"
#         "Domain: Technology automation services for clients.\n"
#         "Services: Automation consulting, process optimization, system development, "
#         "web solutions, API integrations, analytics.\n"
#         "Education: Provides student courses with practical projects and certification support.\n"
#         "Tone: Professional, friendly, clear, concise."
#     )


# def generate_ai_reply(user_message: str) -> str:
#     api_key = getattr(settings, "GEMINI_API_KEY", "")
#     if not api_key:
#         return "AI assistant is not configured yet. Please set GEMINI_API_KEY in environment settings."

#     model_name = getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash")
#     client = genai.Client(api_key=api_key)

#     instruction = (
#         "You are SG.Automix Tech AI assistant.\n"
#         "Rule 1: If the user asks about the company, services, courses, certification, "
#         "or company background, answer from this profile only:\n"
#         f"{_company_profile_text()}\n"
#         "Rule 2: If the user asks something else, answer generally and helpfully.\n"
#         "Rule 3: Keep response short and clear."
#     )

#     prompt = f"{instruction}\n\nUser message: {user_message}"
#     response = client.models.generate_content(model=model_name, contents=prompt)

#     if getattr(response, "text", None):
#         return response.text.strip()

#     return "I could not generate a response right now. Please try again."


# import google.generativeai as genai
# from django.conf import settings


# def _company_profile_text():
#     return (
#         f"Company Name: SG.Automix Tech\n"
#         f"Founded: {getattr(settings, 'COMPANY_START_YEAR', 2026)}\n"
#         "Domain: Technology automation services for clients.\n"
#         "Services: Automation consulting, process optimization, system development, "
#         "web solutions, API integrations, analytics.\n"
#         "Education: Provides student courses with practical projects and certification support.\n"
#         "Tone: Professional, friendly, clear, concise."
#     )


# def generate_ai_reply(user_message: str) -> str:
#     try:
#         # 🔑 API KEY load
#         api_key = getattr(settings, "GEMINI_API_KEY", "")

#         if not api_key:
#             return "AI assistant is not configured yet. Please set GEMINI_API_KEY."

#         # 🔧 Configure Gemini
#         genai.configure(api_key=api_key)

#         # 🤖 Model select
#         model_name = getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash")
#         model = genai.GenerativeModel(model_name)

#         # 🧠 Instruction
#         instruction = (
#             "You are SG.Automix Tech AI assistant.\n"
#             "Rule 1: If the user asks about the company, services, courses, certification, "
#             "or company background, answer ONLY from this profile:\n"
#             f"{_company_profile_text()}\n"
#             "Rule 2: If the user asks something else, answer generally.\n"
#             "Rule 3: Keep response short and clear."
#         )

#         prompt = f"{instruction}\n\nUser message: {user_message}"

#         # 🚀 Generate response
#         response = model.generate_content(prompt)

#         if response and hasattr(response, "text"):
#             return response.text.strip()

#         return "I could not generate a response right now."

#     except Exception as e:
#         print("AI ERROR:", str(e))   # logs me dikhega
#         return "AI service is temporarily unavailable. Please try again later."


"""
SG.Automix Tech — Advanced AI Assistant Service
================================================
Features:
  • Live data fetching from sgautomixtech.info (services, courses, projects, contact)
  • Client query handling (courses, pricing, services, contact info)
  • Caching to avoid repeated fetches in the same session
  • Graceful fallback to static profile if site is unreachable
  • Drop-in replacement: same function signature as original
"""

import time
import re
import threading
from typing import Optional

import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from django.conf import settings


# ── Cache ────────────────────────────────────────────────────────────────────

_cache: dict = {}
_cache_lock = threading.Lock()
CACHE_TTL_SECONDS = 3600          # refresh site data every hour


def _cache_get(key: str) -> Optional[str]:
    with _cache_lock:
        entry = _cache.get(key)
        if entry and (time.time() - entry["ts"]) < CACHE_TTL_SECONDS:
            return entry["value"]
    return None


def _cache_set(key: str, value: str) -> None:
    with _cache_lock:
        _cache[key] = {"value": value, "ts": time.time()}


# ── Page Fetcher ─────────────────────────────────────────────────────────────

BASE_URL = "https://sgautomixtech.info"

PAGES = {
    "home":        "/",
    "about":       "/about/about-us/",
    "services":    "/services/automation-services/",
    "courses":     "/courses/certified-courses/",
    "projects":    "/projects/client-projects/",
    "testimonials": "/testimonial/client-testimonials/",
    "contact":     "/contact/contact-us/",
}

_HEADERS = {
    "User-Agent": "SG-Automix-AI-Bot/2.0 (internal assistant)",
}


def _fetch_page_text(path: str) -> str:
    """Fetch a page and return clean plain text (no HTML tags)."""
    cache_key = f"page:{path}"
    cached = _cache_get(cache_key)
    if cached:
        return cached

    url = BASE_URL + path
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=8)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove nav, footer, scripts, styles
        for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        # Collapse excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        _cache_set(cache_key, text)
        return text
    except Exception as exc:
        return f"[Could not fetch {url}: {exc}]"


def _build_site_context() -> str:
    """Build a comprehensive context block from all public pages."""
    cache_key = "site:full_context"
    cached = _cache_get(cache_key)
    if cached:
        return cached

    parts = []
    for name, path in PAGES.items():
        page_text = _fetch_page_text(path)
        parts.append(f"=== {name.upper()} PAGE ===\n{page_text}\n")

    full_context = "\n".join(parts)
    _cache_set(cache_key, full_context)
    return full_context


# ── Static Fallback Profile ──────────────────────────────────────────────────

def _static_profile() -> str:
    return (
        "Company Name: SG.Automix Tech\n"
        f"Founded: {getattr(settings, 'COMPANY_START_YEAR', 2026)}\n"
        "Domain: Technology automation services for clients.\n"
        "Services: Automation consulting, process optimization, system development, "
        "web solutions, API integrations, analytics, tech training.\n"
        "Education: Certified courses — Graphic Designing (₹3,990), "
        "AI Creation with Python (₹1,099 discounted), practical projects, certification support.\n"
        "Contact Email: support@sgautomixtech.info\n"
        "Contact Phone / WhatsApp: +91 98889 91877\n"
        "Website: https://sgautomixtech.info\n"
        "Tone: Professional, friendly, clear, concise."
    )


# ── Keyword Router ───────────────────────────────────────────────────────────

_TOPIC_KEYWORDS = {
    "services":     ["service", "automation", "consulting", "development", "api", "web", "workflow",
                     "optimization", "process", "software"],
    "courses":      ["course", "class", "learn", "training", "batch", "enroll", "certification",
                     "graphic", "python", "ai course", "price", "₹", "fee", "cost", "discount"],
    "contact":      ["contact", "phone", "email", "whatsapp", "call", "reach", "support",
                     "number", "address", "talk"],
    "projects":     ["project", "portfolio", "work", "client project", "case study"],
    "about":        ["about", "who are you", "company", "founded", "background", "team"],
    "testimonials": ["testimonial", "review", "feedback", "client say", "rating"],
}


def _detect_relevant_pages(user_message: str) -> list[str]:
    """Return which page paths are most relevant to the user's question."""
    lower = user_message.lower()
    relevant = set()

    for topic, keywords in _TOPIC_KEYWORDS.items():
        if any(kw in lower for kw in keywords):
            relevant.add(topic)

    # Always include home as baseline context if nothing matched
    if not relevant:
        relevant.add("home")

    return [PAGES[t] for t in relevant if t in PAGES]


def _build_targeted_context(user_message: str) -> str:
    """Fetch only the pages relevant to this message (faster & focused)."""
    paths = _detect_relevant_pages(user_message)
    parts = []
    for path in paths:
        page_text = _fetch_page_text(path)
        label = [k for k, v in PAGES.items() if v == path]
        label = label[0].upper() if label else path
        parts.append(f"=== {label} PAGE ===\n{page_text}\n")
    return "\n".join(parts)


# ── Contact Info Helper ──────────────────────────────────────────────────────

CONTACT_INFO = {
    "email":     "support@sgautomixtech.info",
    "phone":     "+91 98889 91877",
    "whatsapp":  "https://wa.me/919888991877",
    "website":   "https://sgautomixtech.info",
}

_CONTACT_TRIGGER = re.compile(
    r"\b(contact|phone|email|whatsapp|call|number|reach|support|talk)\b",
    re.IGNORECASE,
)


def _direct_contact_reply(user_message: str) -> Optional[str]:
    """Return a quick contact block without an AI call if the user just asks for contact info."""
    if _CONTACT_TRIGGER.search(user_message) and len(user_message.split()) < 15:
        return (
            "Here is how you can reach **SG.Automix Tech**:\n\n"
            f"📧 **Email:** {CONTACT_INFO['email']}\n"
            f"📞 **Phone / WhatsApp:** {CONTACT_INFO['phone']}\n"
            f"💬 **WhatsApp Link:** {CONTACT_INFO['whatsapp']}\n"
            f"🌐 **Website:** {CONTACT_INFO['website']}\n\n"
            "Feel free to get in touch — we're happy to help!"
        )
    return None


# ── Main Entry Point ─────────────────────────────────────────────────────────

def generate_ai_reply(user_message: str) -> str:
    """
    Generate an AI reply for the given user message.
    Uses live website data + Gemini to answer company and general questions.
    """
    try:
        # ── Quick contact shortcut ──────────────────────────────────────────
        contact_reply = _direct_contact_reply(user_message)
        if contact_reply:
            return contact_reply

        # ── API key ─────────────────────────────────────────────────────────
        api_key = getattr(settings, "GEMINI_API_KEY", "")
        if not api_key:
            return "AI assistant is not configured yet. Please set GEMINI_API_KEY in settings."

        genai.configure(api_key=api_key)

        model_name = getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash")
        model = genai.GenerativeModel(model_name)

        # ── Live context (targeted to this query) ───────────────────────────
        try:
            live_context = _build_targeted_context(user_message)
        except Exception:
            live_context = _static_profile()   # graceful fallback

        # ── System instruction ──────────────────────────────────────────────
        instruction = f"""You are the official AI assistant for SG.Automix Tech.

COMPANY LIVE DATA (fetched from the website right now):
{live_context}

CONTACT INFORMATION (always accurate):
  Email:     {CONTACT_INFO['email']}
  Phone:     {CONTACT_INFO['phone']}
  WhatsApp:  {CONTACT_INFO['whatsapp']}
  Website:   {CONTACT_INFO['website']}

RULES:
1. For questions about the company, services, courses, projects, pricing, certification,
   team, or background — answer ONLY using the live data above.
2. Always provide contact information when the user asks for it.
3. For pricing or course details — give exact figures from the live data.
4. For general knowledge questions (coding, tech, etc.) — answer normally.
5. Keep responses clear, friendly, and concise.
6. If unsure about a specific detail not in the data, say:
   "For the most accurate details, please contact us at {CONTACT_INFO['email']}
   or WhatsApp {CONTACT_INFO['phone']}."
7. Never make up services, prices, or team names not found in the live data.
8. Respond in the same language the user writes in.
"""

        prompt = f"{instruction}\n\nUser: {user_message}"

        # ── Generate ─────────────────────────────────────────────────────────
        response = model.generate_content(prompt)

        if response and hasattr(response, "text") and response.text:
            return response.text.strip()

        return "I could not generate a response right now. Please try again."

    except Exception as exc:
        print(f"[SG.Automix AI ERROR]: {exc}")
        return (
            "AI service is temporarily unavailable. Please try again later, "
            f"or contact us directly at {CONTACT_INFO['email']} "
            f"/ WhatsApp {CONTACT_INFO['phone']}."
        )


# ── Cache Management Utilities ───────────────────────────────────────────────

def clear_ai_cache() -> None:
    """Call this from a management command or admin action to force a site refresh."""
    with _cache_lock:
        _cache.clear()
    print("[SG.Automix AI] Cache cleared — next query will fetch fresh site data.")


def warm_ai_cache() -> None:
    """Pre-warm the cache (call from AppConfig.ready() for faster first response)."""
    import threading

    def _warm():
        try:
            _build_site_context()
            print("[SG.Automix AI] Cache warmed successfully.")
        except Exception as e:
            print(f"[SG.Automix AI] Cache warm failed: {e}")
    threading.Thread(target=_warm, daemon=True).start()
