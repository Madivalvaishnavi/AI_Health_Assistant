
from google import genai


# ============================================================
# AI HEALTH CHATBOT
# ============================================================

def health_chatbot(question, api_key=None):
    """
    AI Health Assistant.

    Features:
    - Predefined responses for common health questions
    - Gemini AI for general health questions
    - Health-focused AI instructions
    - Medical safety guidelines
    - API error handling
    """

    # --------------------------------------------------------
    # VALIDATE QUESTION
    # --------------------------------------------------------

    if not question or not question.strip():
        return "Please enter a health question."

    original_question = question.strip()
    question = original_question.lower()

    # --------------------------------------------------------
    # PREDEFINED HEALTH RESPONSES
    # --------------------------------------------------------

    if "fever" in question:

        return (
            "🌡️ Fever Advice\n\n"
            "Drink plenty of fluids, get enough rest, "
            "and monitor your temperature.\n\n"
            "⚠️ If the fever is severe, persistent, or accompanied "
            "by serious symptoms, consult a qualified healthcare professional."
        )

    elif "headache" in question:

        return (
            "🤕 Headache Advice\n\n"
            "Stay hydrated, get enough rest, and reduce excessive "
            "screen time. Try to maintain regular sleep and meals.\n\n"
            "⚠️ Seek professional medical advice if the headache "
            "is severe, unusual, persistent, or accompanied by other serious symptoms."
        )

    elif "cold" in question or "cough" in question:

        return (
            "🤧 Cold/Cough Advice\n\n"
            "Get enough rest, drink warm fluids, and stay hydrated.\n\n"
            "⚠️ If symptoms become severe, last for a long time, "
            "or cause breathing difficulty, consult a healthcare professional."
        )

    elif "diabetes" in question:

        return (
            "🩸 Diabetes Information\n\n"
            "Diabetes is a condition involving high blood glucose "
            "levels. Healthy eating, physical activity, regular monitoring, "
            "and prescribed treatment can help manage it.\n\n"
            "⚠️ Individual treatment should always be discussed "
            "with a qualified healthcare professional."
        )

    elif "blood pressure" in question or "bp" in question:

        return (
            "❤️ Blood Pressure Information\n\n"
            "Maintaining a balanced diet, regular physical activity, "
            "healthy weight, adequate sleep, and stress management "
            "can support healthy blood pressure.\n\n"
            "⚠️ If you have unusually high or low readings or concerning "
            "symptoms, consult a healthcare professional."
        )

    elif "heart" in question:

        return (
            "❤️ Heart Health Advice\n\n"
            "Regular physical activity, a balanced diet, healthy sleep, "
            "and avoiding tobacco can support heart health.\n\n"
            "⚠️ Chest pain, severe breathing difficulty, fainting, or "
            "other serious symptoms require urgent medical attention."
        )

    elif "covid" in question:

        return (
            "😷 COVID-19 Information\n\n"
            "If you have symptoms of a respiratory infection, rest, "
            "stay hydrated, and follow current public-health guidance.\n\n"
            "⚠️ Seek professional medical advice if symptoms are severe "
            "or getting worse."
        )

    elif "weight" in question:

        return (
            "⚖️ Healthy Weight Advice\n\n"
            "A balanced diet, regular physical activity, adequate sleep, "
            "and sustainable habits can support a healthy weight.\n\n"
            "⚠️ Individual nutritional needs vary, so consult a qualified "
            "healthcare professional for personalized guidance."
        )

    elif "water" in question:

        return (
            "💧 Hydration Advice\n\n"
            "Drink fluids regularly throughout the day. Your needs can "
            "vary depending on activity, weather, diet, and health conditions.\n\n"
            "⚠️ If a healthcare professional has given you a specific "
            "fluid restriction, follow their advice."
        )

    elif "exercise" in question or "fitness" in question:

        return (
            "🏃 Exercise Advice\n\n"
            "Regular physical activity can support overall health. "
            "Start gradually and choose activities appropriate for "
            "your fitness level.\n\n"
            "⚠️ Stop exercising and seek medical advice if you experience "
            "severe chest pain, fainting, or serious breathing difficulty."
        )

    elif "hello" in question or "hi" in question:

        return (
            "👋 Hello!\n\n"
            "I'm your AI Health Assistant. "
            "You can ask me general questions about health, fitness, "
            "nutrition, hydration, or wellness."
        )

    # --------------------------------------------------------
    # GEMINI AI RESPONSE
    # --------------------------------------------------------

    if not api_key:

        return (
            "⚠️ AI service is currently unavailable.\n\n"
            "The Gemini API key has not been configured. "
            "Please configure the API key in Streamlit secrets."
        )

    try:

        # ----------------------------------------------------
        # CREATE GEMINI CLIENT
        # ----------------------------------------------------

        client = genai.Client(
            api_key=api_key
        )

        # ----------------------------------------------------
        # HEALTH-FOCUSED PROMPT
        # ----------------------------------------------------

        prompt = f"""
You are an AI Health Assistant inside a student-built
personal health monitoring application.

Your role is to provide GENERAL health and wellness
information in a safe, clear, and responsible way.

USER QUESTION:
{original_question}

IMPORTANT SAFETY RULES:

1. Do NOT diagnose diseases or medical conditions.
2. Do NOT claim certainty about a user's condition.
3. Do NOT prescribe medicines.
4. Do NOT recommend changing medicine dosage.
5. Do NOT tell users to stop prescribed medicines.
6. Do NOT replace a qualified doctor or healthcare professional.
7. If the question involves serious or concerning symptoms,
   recommend consulting a qualified healthcare professional.
8. If the situation may be an emergency, clearly recommend
   seeking urgent medical attention.
9. Do not provide dangerous or unsafe medical instructions.
10. Keep the response simple and understandable.

RESPONSE FORMAT:

Give the answer using this structure when appropriate:

### 💡 Answer
Provide a clear explanation.

### ✅ General Suggestions
Give safe general wellness suggestions.

### ⚠️ When to Seek Medical Help
Mention when professional medical advice may be appropriate.

Keep the response concise and student-friendly.
"""

        # ----------------------------------------------------
        # GENERATE RESPONSE
        # ----------------------------------------------------

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        # ----------------------------------------------------
        # VALIDATE RESPONSE
        # ----------------------------------------------------

        if response and response.text:

            answer = response.text.strip()

            return (
                answer
                + "\n\n"
                + "⚠️ **Disclaimer:** This information is for "
                "general health awareness only and does not replace "
                "professional medical advice."
            )

        else:

            return (
                "⚠️ The AI did not return a response. "
                "Please try again."
            )

    # --------------------------------------------------------
    # API / NETWORK ERROR
    # --------------------------------------------------------

    except Exception as e:

        error_message = str(e).lower()

        if "api key" in error_message or "authentication" in error_message:

            return (
                "🔑 **AI Authentication Error**\n\n"
                "The Gemini API key could not be authenticated. "
                "Please check your Streamlit secrets configuration."
            )

        elif "quota" in error_message or "429" in error_message:

            return (
                "⏳ **AI Usage Limit Reached**\n\n"
                "The Gemini API usage limit has been reached. "
                "Please try again later."
            )

        elif "404" in error_message or "not found" in error_message:

            return (
                "⚠️ **AI Model Unavailable**\n\n"
                "The configured Gemini model is currently unavailable. "
                "Please check the model configuration."
            )

        elif "connection" in error_message or "network" in error_message:

            return (
                "🌐 **Connection Problem**\n\n"
                "Unable to connect to the AI service right now. "
                "Please check your internet connection and try again."
            )

        else:

            return (
                "⚠️ **AI Service Error**\n\n"
                "The AI assistant could not process your request "
                "right now. Please try again later."
            )

