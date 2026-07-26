# health_report.py

from datetime import datetime


def generate_health_report(fitness_data, medicines):
    """
    Generates a simple health report using
    fitness records and saved medicines.
    """

    # -------------------------------------------------
    # CHECK FITNESS DATA
    # -------------------------------------------------

    if not fitness_data:

        return "No fitness data available to generate a report."


    # -------------------------------------------------
    # CALCULATE TOTALS
    # -------------------------------------------------

    total_steps = 0
    total_calories = 0
    total_water = 0.0

    for record in fitness_data:

        # Database record format:
        # (id, steps, calories, water)

        total_steps += record[1]
        total_calories += record[2]
        total_water += record[3]


    # -------------------------------------------------
    # CALCULATE AVERAGES
    # -------------------------------------------------

    number_of_records = len(fitness_data)

    average_steps = total_steps / number_of_records

    average_calories = total_calories / number_of_records

    average_water = total_water / number_of_records


    # -------------------------------------------------
    # GENERATE REPORT
    # -------------------------------------------------

    report = f"""
🩺 AI PERSONAL HEALTH REPORT
================================

📅 Report Date:
{datetime.now().strftime("%d-%m-%Y %H:%M")}

📊 FITNESS SUMMARY
--------------------------------

👣 Average Daily Steps:
{average_steps:.0f} steps

🔥 Average Calories Burned:
{average_calories:.0f} calories

💧 Average Water Intake:
{average_water:.2f} liters

📋 Total Fitness Records:
{number_of_records}


💊 MEDICATION SUMMARY
--------------------------------
"""


    # -------------------------------------------------
    # ADD MEDICATION INFORMATION
    # -------------------------------------------------

    if medicines:

        report += f"Total Saved Medicines: {len(medicines)}\n\n"

        for medicine in medicines:

            # Database record format:
            # (id, medicine_name, dosage, time)

            report += (
                f"💊 {medicine[1]} | "
                f"Dosage: {medicine[2]} | "
                f"Time: {medicine[3]}\n"
            )

    else:

        report += "No medicines have been saved yet.\n"


    # -------------------------------------------------
    # HEALTH RECOMMENDATIONS
    # -------------------------------------------------

    report += """
    
💡 GENERAL HEALTH RECOMMENDATIONS
--------------------------------
"""

    if average_steps < 5000:

        report += (
            "• Consider gradually increasing your daily physical activity.\n"
        )

    else:

        report += (
            "• Your average step count shows good physical activity.\n"
        )


    if average_water < 2:

        report += (
            "• Consider drinking more water throughout the day, "
            "unless your healthcare professional advises otherwise.\n"
        )

    else:

        report += (
            "• Your recorded water intake looks good. "
            "Continue staying hydrated.\n"
        )


    report += """
    
⚠️ DISCLAIMER
--------------------------------
This report provides general health and wellness information.
It is not a medical diagnosis or a substitute for professional
medical advice. Please consult a qualified healthcare professional
for personal medical concerns.
"""


    return report