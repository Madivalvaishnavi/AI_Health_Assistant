from google import genai


def health_chatbot(question, api_key=None):
    """
    Returns a response to the user's health question.

    First checks predefined responses.
    If no predefined response is found, uses Gemini AI.
    """

    question = question.lower().strip()

    # Existing predefined responses
    if "fever" in question:
        return "Drink plenty of water, take proper rest, and consult a doctor if the fever continues."

    elif "headache" in question:
        return "Stay hydrated, take enough rest, and avoid too much screen time."

    elif "cold" in question or "cough" in question:
        return "Drink warm fluids, get enough rest, and consult a doctor if symptoms become severe."

    elif "diabetes" in question:
        return "Diabetes is a condition where blood sugar levels become too high. A healthy diet, exercise, and medicines help manage it."

    elif "blood pressure" in question or "bp" in question:
        return "High blood pressure can increase the risk of heart disease. Regular exercise and a balanced diet can help."

    elif "heart" in question:
        return "Eat healthy food, exercise regularly, and avoid smoking to maintain heart health."

    elif "covid" in question:
        return "If you have COVID-19 symptoms, isolate yourself and consult a healthcare professional."

    elif "weight" in question:
        return "Maintain a balanced diet and exercise regularly to achieve a healthy weight."

    elif "water" in question:
        return "Drink around 2 to 3 liters of water every day unless advised otherwise by your doctor."

    elif "exercise" in question or "fitness" in question:
        return "Aim for at least 30 minutes of moderate exercise on most days of the week."

    elif "hello" in question or "hi" in question:
        return "Hello! How can I help you with your health today?"

    # If no predefined response is found, use Gemini AI
    else:

        if not api_key:
            return "Sorry, I don't have information about that. Please consult a healthcare professional for medical advice."

        try:

            client = genai.Client(
                api_key=api_key
            )

            prompt = f"""
You are an AI Health Assistant for a student project.

Answer the user's question with general health and wellness information.

Important rules:
- Do not diagnose diseases.
- Do not prescribe medicines.
- Do not recommend changing medication doses.
- For serious symptoms, emergencies, or personal medical concerns,
  advise the user to consult a qualified healthcare professional.
- Keep the answer simple and easy to understand.

User's question:
{question}
"""

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            return f"AI Error: {str(e)}"