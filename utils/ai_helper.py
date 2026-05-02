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



import google.generativeai as genai
from django.conf import settings


def _company_profile_text():
    return (
        f"Company Name: SG.Automix Tech\n"
        f"Founded: {getattr(settings, 'COMPANY_START_YEAR', 2026)}\n"
        "Domain: Technology automation services for clients.\n"
        "Services: Automation consulting, process optimization, system development, "
        "web solutions, API integrations, analytics.\n"
        "Education: Provides student courses with practical projects and certification support.\n"
        "Tone: Professional, friendly, clear, concise."
    )


def generate_ai_reply(user_message: str) -> str:
    try:
        # 🔑 API KEY load
        api_key = getattr(settings, "GEMINI_API_KEY", "")

        if not api_key:
            return "AI assistant is not configured yet. Please set GEMINI_API_KEY."

        # 🔧 Configure Gemini
        genai.configure(api_key=api_key)

        # 🤖 Model select
        model_name = getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash")
        model = genai.GenerativeModel(model_name)

        # 🧠 Instruction
        instruction = (
            "You are SG.Automix Tech AI assistant.\n"
            "Rule 1: If the user asks about the company, services, courses, certification, "
            "or company background, answer ONLY from this profile:\n"
            f"{_company_profile_text()}\n"
            "Rule 2: If the user asks something else, answer generally.\n"
            "Rule 3: Keep response short and clear."
        )

        prompt = f"{instruction}\n\nUser message: {user_message}"

        # 🚀 Generate response
        response = model.generate_content(prompt)

        if response and hasattr(response, "text"):
            return response.text.strip()

        return "I could not generate a response right now."

    except Exception as e:
        print("AI ERROR:", str(e))   # logs me dikhega
        return "AI service is temporarily unavailable. Please try again later."