from google import genai


MODEL_NAME = "gemini-3.7-flash"


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

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if response and response.text:
            return response.text.strip()

        return "Sorry, I could not generate a response."

    except Exception as e:

        error = str(e)

        if "429" in error or "RESOURCE_EXHAUSTED" in error:
            return (
                "The Gemini API quota has been reached or "
                "the service is temporarily busy. Please try again later."
            )

        if "404" in error or "NOT_FOUND" in error:
            return (
                "The Gemini model is unavailable. "
                "Please check the Gemini model configuration."
            )

        return "Gemini connection error: " + error