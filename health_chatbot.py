def health_chatbot(question):

    question = question.lower()

    if "fever" in question:
        return "Drink plenty of water and consult a doctor if symptoms continue."

    elif "headache" in question:
        return "Take proper rest and stay hydrated."

    elif "diabetes" in question:
        return "Diabetes is a condition where blood sugar levels become too high."

    else:
        return "Please consult a healthcare professional for medical advice."