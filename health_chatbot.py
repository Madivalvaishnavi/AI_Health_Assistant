from google import genai
import time


# ============================================================
# GEMINI MODELS
# ============================================================

PRIMARY_MODEL = "gemini-3.8-flash"
FALLBACK_MODEL = "gemini-3.5-flash-lite"


# ============================================================
# AI HEALTH CHATBOT
# ============================================================

def health_chatbot(question, api_key):

    if not question or not question.strip():
        return "Please enter a health question."

    if not api_key:
        return "Gemini API key is missing."

    try:

        client = genai.Client(
            api_key=api_key
        )

        prompt = f"""
You are an AI Health Assistant.

Help the user with general health and wellness questions.

User question:
{question}

Give a clear and simple answer.

Rules:
- Answer the user's question directly.
- Use simple language.
- If symptoms are mentioned, explain possible common causes.
- Do not claim a definite diagnosis.
- Give safe general advice.
- Tell the user when they should consult a doctor.
- If the situation appears to be an emergency, advise the
  user to seek emergency medical care immediately.
- Do not pretend to be a real doctor.
- Do not prescribe prescription medicines.
- For medicine questions, give general information and advise
  consulting a doctor or pharmacist for dosage and suitability.

This information is for general educational purposes and
does not replace professional medical advice.
"""

        # ====================================================
        # TRY PRIMARY MODEL
        # ====================================================

        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model=PRIMARY_MODEL,
                    contents=prompt
                )

                if response and response.text:
                    return response.text.strip()

            except Exception as e:

                error = str(e)

                if "503" in error or "UNAVAILABLE" in error:

                    if attempt < 2:
                        time.sleep(2 ** attempt)
                        continue

                    break

                if "429" in error or "RESOURCE_EXHAUSTED" in error:

                    break

                if "404" in error or "NOT_FOUND" in error:

                    break

                return "Gemini connection error: " + error

        # ====================================================
        # FALLBACK MODEL
        # ====================================================

        try:

            response = client.models.generate_content(
                model=FALLBACK_MODEL,
                contents=prompt
            )

            if response and response.text:
                return response.text.strip()

        except Exception as e:

            error = str(e)

            if "429" in error or "RESOURCE_EXHAUSTED" in error:
                return (
                    "Gemini API quota has been reached. "
                    "Please try again later."
                )

            if "503" in error or "UNAVAILABLE" in error:
                return (
                    "Gemini is temporarily busy right now. "
                    "Please try again in a few moments."
                )

            if "404" in error or "NOT_FOUND" in error:
                return (
                    "The Gemini model is currently unavailable. "
                    "Please check the Gemini API configuration."
                )

            return "Gemini connection error: " + error

        return "Sorry, I could not generate a response."

    except Exception as e:

        return "Gemini connection error: " + str(e)