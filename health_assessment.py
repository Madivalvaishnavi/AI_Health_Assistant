
# ============================================================
# API-FREE HEALTH ASSESSMENT
# ============================================================

def assess_symptoms(symptoms):
    """
    Local rule-based symptom assessment.

    This is NOT a medical diagnosis.
    No API key required.
    """

    if not symptoms or not symptoms.strip():
        return "Please describe what you are feeling."

    text = symptoms.lower().strip()

    # --------------------------------------------------------
    # EMERGENCY CHECK
    # --------------------------------------------------------

    emergency_keywords = [
        "severe chest pain",
        "chest pain",
        "can't breathe",
        "cannot breathe",
        "difficulty breathing",
        "not breathing",
        "unconscious",
        "fainted",
        "seizure",
        "stroke",
        "severe bleeding"
    ]

    if any(word in text for word in emergency_keywords):

        return (
            "🚨 **POSSIBLE MEDICAL EMERGENCY**\n\n"
            "🩺 POSSIBLE HEALTH ISSUE / CATEGORY\n"
            "The symptoms you described may require urgent medical evaluation. "
            "A chatbot cannot determine the cause safely.\n\n"
            "👨‍⚕️ SUGGESTED DOCTOR / SPECIALIST\n"
            "Emergency medical services or the nearest emergency department.\n\n"
            "💊 GENERAL MEDICATION GUIDANCE\n"
            "Do not rely on this assessment to choose or change medication "
            "during a possible emergency.\n\n"
            "🏠 HOME REMEDIES\n"
            "Do not delay emergency medical care in order to try home remedies.\n\n"
            "⚠️ PRECAUTIONS\n"
            "Avoid driving yourself if you are severely unwell or impaired. "
            "Seek immediate assistance.\n\n"
            "👉 WHAT TO DO NEXT\n"
            "Contact your local emergency service or get to the nearest "
            "emergency department immediately.\n\n"
            "🚨 WHEN TO SEEK URGENT MEDICAL HELP\n"
            "Now. Do not wait for the symptoms to improve."
        )

    # --------------------------------------------------------
    # FEVER
    # --------------------------------------------------------

    has_fever = (
        "fever" in text
        or "high temperature" in text
        or "temperature" in text
    )

    has_headache = (
        "headache" in text
        or "head pain" in text
    )

    has_cough = (
        "cough" in text
        or "cold" in text
        or "sore throat" in text
    )

    has_stomach = (
        "stomach pain" in text
        or "abdominal pain" in text
        or "vomiting" in text
        or "diarrhea" in text
    )

    has_fatigue = (
        "tired" in text
        or "fatigue" in text
        or "weakness" in text
    )

    has_body_pain = (
        "body pain" in text
        or "muscle pain" in text
        or "body ache" in text
    )

    # --------------------------------------------------------
    # RESPIRATORY / COLD CATEGORY
    # --------------------------------------------------------

    if has_fever and has_cough:

        return (
            "🩺 POSSIBLE HEALTH ISSUE / CATEGORY\n"
            "Your symptoms may fit a general respiratory or infectious "
            "illness pattern. The exact cause cannot be determined from "
            "symptoms alone.\n\n"

            "👨‍⚕️ SUGGESTED DOCTOR / SPECIALIST\n"
            "A General Physician / Primary Care Doctor can evaluate "
            "these symptoms.\n\n"

            "💊 GENERAL MEDICATION GUIDANCE\n"
            "Do not start prescription medication based on this assessment. "
            "A doctor or pharmacist can advise whether any over-the-counter "
            "treatment is appropriate for you.\n\n"

            "🏠 HOME REMEDIES\n"
            "• Rest adequately.\n"
            "• Drink enough fluids.\n"
            "• Prefer comfortable warm fluids if they feel soothing.\n"
            "• Monitor your temperature and symptoms.\n\n"

            "⚠️ PRECAUTIONS\n"
            "Avoid self-prescribing antibiotics or changing prescribed "
            "medicines without professional advice.\n\n"

            "👉 WHAT TO DO NEXT\n"
            "Monitor your symptoms and consider consulting a doctor, "
            "especially if symptoms persist or worsen.\n\n"

            "🚨 WHEN TO SEEK URGENT MEDICAL HELP\n"
            "Seek urgent help for severe breathing difficulty, chest pain, "
            "confusion, fainting, severe weakness, or rapid worsening."
        )

    # --------------------------------------------------------
    # FEVER + HEADACHE
    # --------------------------------------------------------

    if has_fever and has_headache:

        return (
            "🩺 POSSIBLE HEALTH ISSUE / CATEGORY\n"
            "Fever with headache can occur with several illnesses, including "
            "common infections. The exact cause requires clinical evaluation.\n\n"

            "👨‍⚕️ SUGGESTED DOCTOR / SPECIALIST\n"
            "A General Physician / Primary Care Doctor.\n\n"

            "💊 GENERAL MEDICATION GUIDANCE\n"
            "A pharmacist or doctor can advise whether an appropriate "
            "over-the-counter fever or pain medicine is suitable for you. "
            "Do not exceed label directions.\n\n"

            "🏠 HOME REMEDIES\n"
            "• Rest.\n"
            "• Drink fluids.\n"
            "• Monitor temperature.\n"
            "• Eat light meals if comfortable.\n\n"

            "⚠️ PRECAUTIONS\n"
            "Avoid taking multiple medicines containing the same active "
            "ingredient unless a healthcare professional advises it.\n\n"

            "👉 WHAT TO DO NEXT\n"
            "Monitor symptoms and seek medical advice if they persist "
            "or worsen.\n\n"

            "🚨 WHEN TO SEEK URGENT MEDICAL HELP\n"
            "Seek urgent care for a sudden severe headache, confusion, "
            "fainting, seizures, stiff neck with severe illness, or "
            "difficulty breathing."
        )

    # --------------------------------------------------------
    # HEADACHE
    # --------------------------------------------------------

    if has_headache:

        return (
            "🩺 POSSIBLE HEALTH ISSUE / CATEGORY\n"
            "Your symptoms may be consistent with a common headache pattern. "
            "There are many possible causes, so this is not a diagnosis.\n\n"

            "👨‍⚕️ SUGGESTED DOCTOR / SPECIALIST\n"
            "A General Physician / Primary Care Doctor if the headache "
            "is persistent, recurrent, or concerning.\n\n"

            "💊 GENERAL MEDICATION GUIDANCE\n"
            "A pharmacist can advise whether an over-the-counter pain "
            "reliever is appropriate for you. Follow the product label "
            "and consider your other medicines and health conditions.\n\n"

            "🏠 HOME REMEDIES\n"
            "• Drink water.\n"
            "• Rest in a quiet environment.\n"
            "• Get adequate sleep.\n"
            "• Take breaks from screens.\n\n"

            "⚠️ PRECAUTIONS\n"
            "Avoid repeatedly using pain medicines without medical advice "
            "for frequent headaches.\n\n"

            "👉 WHAT TO DO NEXT\n"
            "Rest and monitor the symptoms. Consult a healthcare professional "
            "if headaches are frequent or persistent.\n\n"

            "🚨 WHEN TO SEEK URGENT MEDICAL HELP\n"
            "Seek urgent help for a sudden extremely severe headache, "
            "confusion, fainting, weakness, speech problems, vision problems, "
            "or headache following a serious injury."
        )

    # --------------------------------------------------------
    # COLD / COUGH
    # --------------------------------------------------------

    if has_cough:

        return (
            "🩺 POSSIBLE HEALTH ISSUE / CATEGORY\n"
            "Your symptoms may fit a common cold or respiratory illness pattern. "
            "The exact cause cannot be confirmed here.\n\n"

            "👨‍⚕️ SUGGESTED DOCTOR / SPECIALIST\n"
            "A General Physician / Primary Care Doctor.\n\n"

            "💊 GENERAL MEDICATION GUIDANCE\n"
            "Ask a pharmacist about suitable over-the-counter options "
            "if needed. Avoid self-prescribing antibiotics.\n\n"

            "🏠 HOME REMEDIES\n"
            "• Rest well.\n"
            "• Drink warm fluids.\n"
            "• Stay hydrated.\n"
            "• Avoid smoke and other irritants.\n\n"

            "⚠️ PRECAUTIONS\n"
            "Monitor breathing and whether symptoms are getting worse.\n\n"

            "👉 WHAT TO DO NEXT\n"
            "Continue supportive care and seek medical advice if symptoms "
            "persist or worsen.\n\n"

            "🚨 WHEN TO SEEK URGENT MEDICAL HELP\n"
            "Seek urgent care for severe breathing difficulty, chest pain, "
            "confusion, fainting, or rapidly worsening symptoms."
        )

    # --------------------------------------------------------
    # STOMACH
    # --------------------------------------------------------

    if has_stomach:

        return (
            "🩺 POSSIBLE HEALTH ISSUE / CATEGORY\n"
            "Your symptoms may relate to a digestive or gastrointestinal issue. "
            "Many different conditions can cause similar symptoms.\n\n"

            "👨‍⚕️ SUGGESTED DOCTOR / SPECIALIST\n"
            "Start with a General Physician. A specialist may be recommended "
            "if the problem persists.\n\n"

            "💊 GENERAL MEDICATION GUIDANCE\n"
            "Medication depends on the cause. Consult a doctor or pharmacist "
            "before taking medicines for persistent stomach symptoms.\n\n"

            "🏠 HOME REMEDIES\n"
            "• Drink fluids regularly.\n"
            "• Eat light foods if tolerated.\n"
            "• Avoid foods that clearly worsen your symptoms.\n"
            "• Rest adequately.\n\n"

            "⚠️ PRECAUTIONS\n"
            "Monitor for dehydration, severe pain, blood in vomit or stool, "
            "or persistent vomiting.\n\n"

            "👉 WHAT TO DO NEXT\n"
            "If symptoms continue or become worse, consult a healthcare professional.\n\n"

            "🚨 WHEN TO SEEK URGENT MEDICAL HELP\n"
            "Seek urgent care for severe abdominal pain, significant bleeding, "
            "fainting, severe dehydration, or serious worsening."
        )

    # --------------------------------------------------------
    # FATIGUE
    # --------------------------------------------------------

    if has_fatigue:

        return (
            "🩺 POSSIBLE HEALTH ISSUE / CATEGORY\n"
            "Tiredness or fatigue can have many possible causes, including "
            "poor sleep, stress, lifestyle factors, infections, and medical conditions.\n\n"

            "👨‍⚕️ SUGGESTED DOCTOR / SPECIALIST\n"
            "A General Physician / Primary Care Doctor if fatigue is persistent.\n\n"

            "💊 GENERAL MEDICATION GUIDANCE\n"
            "Do not use supplements or medicines specifically for fatigue "
            "without professional advice.\n\n"

            "🏠 HOME REMEDIES\n"
            "• Maintain a regular sleep schedule.\n"
            "• Stay hydrated.\n"
            "• Eat balanced meals.\n"
            "• Include suitable physical activity.\n\n"

            "⚠️ PRECAUTIONS\n"
            "Monitor whether fatigue is persistent or associated with other symptoms.\n\n"

            "👉 WHAT TO DO NEXT\n"
            "If fatigue continues, affects daily activities, or keeps returning, "
            "consult a healthcare professional.\n\n"

            "🚨 WHEN TO SEEK URGENT MEDICAL HELP\n"
            "Seek urgent care if severe weakness occurs with chest pain, "
            "breathing difficulty, fainting, confusion, or other serious symptoms."
        )

    # --------------------------------------------------------
    # BODY PAIN
    # --------------------------------------------------------

    if has_body_pain:

        return (
            "🩺 POSSIBLE HEALTH ISSUE / CATEGORY\n"
            "Body or muscle pain can occur after physical activity, illness, "
            "stress, or for many other reasons.\n\n"

            "👨‍⚕️ SUGGESTED DOCTOR / SPECIALIST\n"
            "A General Physician if pain is unexplained, persistent, or severe.\n\n"

            "💊 GENERAL MEDICATION GUIDANCE\n"
            "Ask a pharmacist or doctor about appropriate pain-relief options "
            "based on your health history and other medicines.\n\n"

            "🏠 HOME REMEDIES\n"
            "• Rest the affected area.\n"
            "• Gentle movement may help when appropriate.\n"
            "• Stay hydrated.\n\n"

            "⚠️ PRECAUTIONS\n"
            "Avoid activities that significantly increase the pain.\n\n"

            "👉 WHAT TO DO NEXT\n"
            "Monitor the pain and consult a healthcare professional if it "
            "does not improve or keeps returning.\n\n"

            "🚨 WHEN TO SEEK URGENT MEDICAL HELP\n"
            "Seek urgent care if severe pain occurs with chest pain, "
            "breathing difficulty, fainting, severe weakness, or injury."
        )

    # --------------------------------------------------------
    # GENERAL
    # --------------------------------------------------------

    return (
        "🩺 POSSIBLE HEALTH ISSUE / CATEGORY\n"
        "The symptoms you described do not match a specific local assessment "
        "category. Symptoms alone cannot safely determine a diagnosis.\n\n"

        "👨‍⚕️ SUGGESTED DOCTOR / SPECIALIST\n"
        "A General Physician / Primary Care Doctor is a good starting point.\n\n"

        "💊 GENERAL MEDICATION GUIDANCE\n"
        "Do not start or change medication based only on this assessment. "
        "Ask a doctor or pharmacist for advice.\n\n"

        "🏠 HOME REMEDIES\n"
        "• Rest adequately.\n"
        "• Stay hydrated.\n"
        "• Eat balanced meals.\n"
        "• Monitor your symptoms.\n\n"

        "⚠️ PRECAUTIONS\n"
        "Pay attention to symptoms that become severe, persistent, or unusual.\n\n"

        "👉 WHAT TO DO NEXT\n"
        "If your symptoms continue or worsen, consult a qualified healthcare professional.\n\n"

        "🚨 WHEN TO SEEK URGENT MEDICAL HELP\n"
        "Seek urgent care for severe breathing difficulty, chest pain, "
        "fainting, confusion, seizures, severe bleeding, or rapidly worsening symptoms."
    )


# ============================================================
# OVERALL HEALTH ASSESSMENT
# ============================================================

def assess_overall_health():
    """
    Generates a local overall health assessment.

    No API required.
    """

    try:
        from health_api import (
            get_steps,
            get_calories,
            get_water
        )

        steps = get_steps()
        calories = get_calories()
        water = get_water()

    except Exception:
        steps = 0
        calories = 0
        water = 0

    try:
        from medicine import calculate_adherence

        adherence = calculate_adherence()

    except Exception:
        adherence = 0

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    steps_score = min((steps / 10000) * 100, 100)
    calories_score = min((calories / 500) * 100, 100)
    water_score = min((water / 3) * 100, 100)
    adherence_score = min(adherence, 100)

    score = (
        steps_score * 0.25
        + calories_score * 0.20
        + water_score * 0.25
        + adherence_score * 0.30
    )

    score = round(score)

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if score < 20:
        status = "😟 Needs Attention"
    elif score < 40:
        status = "😐 Getting Started"
    elif score < 60:
        status = "🙂 Fair"
    elif score < 80:
        status = "😊 Good"
    else:
        status = "💪 Excellent"

    # --------------------------------------------------------
    # OBSERVATIONS
    # --------------------------------------------------------

    observations = []

    if steps < 5000:
        observations.append(
            "🚶 Your step count is below the 10,000-step daily goal."
        )
    else:
        observations.append(
            "🚶 Your physical activity is moving toward the daily goal."
        )

    if water < 1.5:
        observations.append(
            "💧 Your recorded water intake is below the 3 L goal."
        )
    else:
        observations.append(
            "💧 Your recorded water intake is progressing toward the goal."
        )

    if calories < 250:
        observations.append(
            "🔥 Your recorded activity calories are currently low."
        )
    else:
        observations.append(
            "🔥 Your recorded calorie activity is progressing."
        )

    if adherence < 80:
        observations.append(
            "💊 Medication adherence is below 80%; continue monitoring it."
        )
    else:
        observations.append(
            "💊 Medication adherence is currently good."
        )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    return (
        f"❤️ **OVERALL HEALTH STATUS**\n"
        f"{status} — Wellness Score: **{score}%**\n\n"

        "📊 **HEALTH OBSERVATIONS**\n"
        + "\n".join(f"• {item}" for item in observations)
        + "\n\n"

        "⚠️ **AREAS THAT MAY NEED ATTENTION**\n"
        f"• Steps: {steps:,} / 10,000\n"
        f"• Water: {water} L / 3 L\n"
        f"• Calories: {calories} / 500\n"
        f"• Medication Adherence: {adherence:.0f}%\n\n"

        "💡 **HEALTH SUGGESTIONS**\n"
        "• Stay physically active according to your ability.\n"
        "• Maintain adequate hydration unless you have a medical fluid restriction.\n"
        "• Maintain balanced meals and regular sleep.\n"
        "• Continue tracking your health goals.\n\n"

        "💊 **MEDICATION / ADHERENCE**\n"
        f"Your current recorded medication adherence is {adherence:.0f}%. "
        "Continue following your healthcare professional's instructions.\n\n"

        "👨‍⚕️ **WHEN TO CONSULT A DOCTOR**\n"
        "Consult a healthcare professional for persistent, worsening, "
        "or concerning symptoms. This wellness assessment is not a diagnosis."
    )
