def calculate_health_risk(
    steps,
    water,
    calories,
    medication_adherence
):
    """
    Calculates a basic health risk level
    using fitness and medication data.

    This is for educational purposes only.
    """

    warnings = []
    risk_score = 0

    # -----------------------------
    # STEPS CHECK
    # -----------------------------

    if steps < 3000:
        risk_score += 2
        warnings.append(
            "🚶 Very low physical activity detected."
        )

    elif steps < 5000:
        risk_score += 1
        warnings.append(
            "🚶 Physical activity is below the recommended goal."
        )

    # -----------------------------
    # WATER CHECK
    # -----------------------------

    if water < 1.5:
        risk_score += 2
        warnings.append(
            "💧 Water intake is quite low."
        )

    elif water < 2:
        risk_score += 1
        warnings.append(
            "💧 Consider increasing your water intake."
        )

    # -----------------------------
    # CALORIES CHECK
    # -----------------------------

    if calories < 300:
        risk_score += 1
        warnings.append(
            "🔥 Recorded calorie-burn level is low."
        )

    # -----------------------------
    # MEDICATION ADHERENCE
    # -----------------------------

    if medication_adherence < 60:
        risk_score += 2
        warnings.append(
            "💊 Medication adherence is very low."
        )

    elif medication_adherence < 80:
        risk_score += 1
        warnings.append(
            "💊 Medication adherence is below 80%."
        )

    # -----------------------------
    # RISK LEVEL
    # -----------------------------

    if risk_score >= 5:
        risk_level = "🔴 High Risk"

    elif risk_score >= 2:
        risk_level = "🟡 Moderate Risk"

    else:
        risk_level = "🟢 Low Risk"

    return risk_level, risk_score, warnings