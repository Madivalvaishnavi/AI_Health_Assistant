# health_report.py

from datetime import datetime


def generate_health_report(
    fitness_data,
    medicines,
    adherence=0,
    steps_goal=10000,
    water_goal=3.0,
    calories_goal=500
):
    """
    Generates a personal health and wellness report.

    This report is for educational purposes only
    and is not a medical diagnosis.
    """

    # ============================================================
    # CHECK FITNESS DATA
    # ============================================================

    if not fitness_data:
        return "No fitness data available to generate a health report."

    # ============================================================
    # FITNESS CALCULATIONS
    # ============================================================

    total_steps = 0
    total_calories = 0
    total_water = 0.0

    for record in fitness_data:

        total_steps += record[1]
        total_calories += record[2]
        total_water += record[3]

    number_of_records = len(fitness_data)

    average_steps = total_steps / number_of_records
    average_calories = total_calories / number_of_records
    average_water = total_water / number_of_records

    # ============================================================
    # GOAL PROGRESS
    # ============================================================

    steps_progress = min(
        (average_steps / steps_goal) * 100,
        100
    )

    water_progress = min(
        (average_water / water_goal) * 100,
        100
    )

    calories_progress = min(
        (average_calories / calories_goal) * 100,
        100
    )

    # ============================================================
    # REPORT HEADER
    # ============================================================

    report = f"""
============================================================
🩺 AI PERSONAL HEALTH REPORT
============================================================

📅 Report Date:
{datetime.now().strftime("%d-%m-%Y %H:%M")}

📋 Report Type:
Personal Health & Wellness Summary


============================================================
🏃 FITNESS SUMMARY
============================================================

👣 Average Steps:
{average_steps:.0f} steps/day

🔥 Average Calories Burned:
{average_calories:.0f} calories/day

💧 Average Water Intake:
{average_water:.2f} liters/day

📋 Total Fitness Records:
{number_of_records}


============================================================
🎯 HEALTH GOAL PROGRESS
============================================================

👣 Steps Goal:
{steps_goal} steps

Progress:
{steps_progress:.1f}%

💧 Water Goal:
{water_goal:.1f} liters

Progress:
{water_progress:.1f}%

🔥 Calories Goal:
{calories_goal} calories

Progress:
{calories_progress:.1f}%


============================================================
💊 MEDICATION SUMMARY
============================================================
"""

    # ============================================================
    # MEDICATION INFORMATION
    # ============================================================

    if medicines:

        report += (
            f"\n💊 Total Active Medicines: "
            f"{len(medicines)}\n\n"
        )

        for medicine in medicines:

            report += (
                f"💊 Medicine: {medicine[1]}\n"
                f"   Dosage: {medicine[2]}\n"
                f"   Time: {medicine[3]}\n\n"
            )

    else:

        report += (
            "\nNo active medicines have been saved.\n"
        )

    # ============================================================
    # MEDICATION ADHERENCE
    # ============================================================

    report += f"""
============================================================
📊 MEDICATION ADHERENCE
============================================================

💊 Overall Medication Adherence:
{adherence:.1f}%

"""

    if adherence >= 80:

        report += (
            "✅ Medication adherence is currently good.\n"
        )

    elif adherence > 0:

        report += (
            "⚠️ Medication adherence is below 80%.\n"
        )

    else:

        report += (
            "ℹ️ No medication adherence records are available.\n"
        )

    # ============================================================
    # HEALTH INSIGHTS
    # ============================================================

    report += """
============================================================
💡 HEALTH INSIGHTS
============================================================
"""

    if average_steps < 5000:

        report += (
            "• Your average step count is relatively low. "
            "Consider gradually increasing daily physical activity.\n"
        )

    elif average_steps < steps_goal:

        report += (
            "• Your activity level is moderate. "
            "Consider gradually moving toward your daily step goal.\n"
        )

    else:

        report += (
            "• Your average step count is meeting or "
            "exceeding your daily goal.\n"
        )

    if average_water < water_goal:

        report += (
            "• Your water intake is below your configured "
            "daily hydration goal.\n"
        )

    else:

        report += (
            "• Your recorded water intake is meeting your "
            "configured daily goal.\n"
        )

    if average_calories < calories_goal:

        report += (
            "• Your recorded calorie-burn level is below "
            "your configured goal.\n"
        )

    else:

        report += (
            "• Your recorded calorie-burn level is meeting "
            "or exceeding your configured goal.\n"
        )

    # ============================================================
    # GENERAL RECOMMENDATIONS
    # ============================================================

    report += """
============================================================
🩺 GENERAL WELLNESS RECOMMENDATIONS
============================================================

"""

    recommendations = []

    if average_steps < steps_goal:

        recommendations.append(
            "Gradually increase daily physical activity "
            "according to your fitness level."
        )

    if average_water < water_goal:

        recommendations.append(
            "Maintain regular water intake throughout the day."
        )

    if adherence < 80 and adherence > 0:

        recommendations.append(
            "Maintain a consistent medication routine and "
            "follow instructions from your healthcare professional."
        )

    if not recommendations:

        recommendations.append(
            "Continue maintaining your current healthy habits "
            "and monitor your health data regularly."
        )

    for recommendation in recommendations:

        report += f"• {recommendation}\n"

    # ============================================================
    # DISCLAIMER
    # ============================================================

    report += """
============================================================
⚠️ MEDICAL DISCLAIMER
============================================================

This report provides general health and wellness information
based on the data entered into the application.

It is NOT a medical diagnosis and should not replace advice,
diagnosis, or treatment from a qualified healthcare professional.

For serious symptoms, emergencies, medication concerns, or
personal medical decisions, please consult a qualified doctor
or pharmacist.

============================================================
🩺 END OF HEALTH REPORT
============================================================
"""

    return report