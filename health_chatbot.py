def health_chatbot(question):
    """
    Returns a simple response based on the user's health question.
    """

    question = question.lower().strip()

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

    else:
        return "Sorry, I don't have information about that. Please consult a healthcare professional for medical advice."