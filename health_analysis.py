import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# ANALYZE FITNESS DATA
# ============================================================

def analyze_fitness_data(fitness_data):
    """
    Analyzes fitness data and returns
    averages and basic health insights.
    """

    if not fitness_data:
        return None, []

    # Convert database records into DataFrame
    df = pd.DataFrame(
        fitness_data,
        columns=["ID", "Steps", "Calories", "Water"]
    )

    # Calculate averages
    average_steps = df["Steps"].mean()
    average_calories = df["Calories"].mean()
    average_water = df["Water"].mean()

    insights = []

    # --------------------------------------------------------
    # STEP INSIGHT
    # --------------------------------------------------------

    if average_steps < 5000:

        insights.append(
            "🚶 Your average step count is low. "
            "Try to include more walking in your daily routine."
        )

    elif average_steps < 10000:

        insights.append(
            "👣 Your average step count is moderate. "
            "Try gradually increasing your daily activity."
        )

    else:

        insights.append(
            "✅ Your average step count is good. "
            "Keep staying active!"
        )

    # --------------------------------------------------------
    # WATER INSIGHT
    # --------------------------------------------------------

    if average_water < 2:

        insights.append(
            "💧 Your average water intake is below 2 liters. "
            "Remember to stay hydrated, unless your healthcare "
            "professional has advised a different amount."
        )

    elif average_water < 3:

        insights.append(
            "💧 Your water intake is moderate. "
            "Continue drinking water regularly throughout the day."
        )

    else:

        insights.append(
            "✅ Your recorded water intake looks good. "
            "Keep maintaining healthy hydration habits."
        )

    # --------------------------------------------------------
    # CALORIE INSIGHT
    # --------------------------------------------------------

    if average_calories < 300:

        insights.append(
            "🔥 Your recorded calorie expenditure is relatively low. "
            "Consider maintaining regular physical activity."
        )

    elif average_calories < 500:

        insights.append(
            "🔥 Your calorie expenditure shows some activity. "
            "Continue maintaining a regular exercise routine."
        )

    else:

        insights.append(
            "✅ Your recorded calorie expenditure shows "
            "regular physical activity."
        )

    return {
        "average_steps": round(average_steps, 2),
        "average_calories": round(average_calories, 2),
        "average_water": round(average_water, 2)
    }, insights


# ============================================================
# MEDICATION INSIGHTS
# ============================================================

def generate_medication_insights(adherence):
    """
    Generates health recommendations based on
    medication adherence percentage.
    """

    insights = []

    if adherence >= 90:

        insights.append(
            "💊 Excellent medication adherence! "
            "Keep following your prescribed medication schedule."
        )

    elif adherence >= 80:

        insights.append(
            "💊 Your medication adherence is good. "
            "Try to maintain your current routine."
        )

    elif adherence > 0:

        insights.append(
            "⚠️ Your medication adherence is below 80%. "
            "Try to follow your medication schedule more consistently."
        )

    else:

        insights.append(
            "ℹ️ No medication adherence records are available yet."
        )

    return insights


# ============================================================
# WELLNESS GOAL INSIGHTS
# ============================================================

def generate_goal_insights(
    steps,
    steps_goal,
    water,
    water_goal,
    calories,
    calories_goal
):
    """
    Generates recommendations based on wellness goals.
    """

    insights = []

    # --------------------------------------------------------
    # STEPS GOAL
    # --------------------------------------------------------

    if steps >= steps_goal:

        insights.append(
            "🎯 You have reached your daily steps goal. "
            "Great job staying active!"
        )

    else:

        remaining_steps = steps_goal - steps

        insights.append(
            f"👣 You need approximately "
            f"{remaining_steps:.0f} more steps to reach your daily goal."
        )

    # --------------------------------------------------------
    # WATER GOAL
    # --------------------------------------------------------

    if water >= water_goal:

        insights.append(
            "🎯 You have reached your daily water goal. "
            "Keep maintaining healthy hydration habits."
        )

    else:

        remaining_water = water_goal - water

        insights.append(
            f"💧 You need about "
            f"{remaining_water:.2f} more liters to reach your water goal."
        )

    # --------------------------------------------------------
    # CALORIES GOAL
    # --------------------------------------------------------

    if calories >= calories_goal:

        insights.append(
            "🎯 You have reached your daily calorie activity goal."
        )

    else:

        remaining_calories = calories_goal - calories

        insights.append(
            f"🔥 You need approximately "
            f"{remaining_calories:.0f} more calories "
            f"to reach your activity goal."
        )

    return insights


# ============================================================
# COMBINED HEALTH INSIGHTS
# ============================================================

def generate_health_insights(
    fitness_data,
    medication_adherence=0,
    steps_goal=10000,
    water_goal=3.0,
    calories_goal=500
):
    """
    Generates combined health insights and recommendations
    from fitness, medication, and wellness goal data.
    """

    all_insights = []

    # --------------------------------------------------------
    # FITNESS INSIGHTS
    # --------------------------------------------------------

    analysis, fitness_insights = analyze_fitness_data(
        fitness_data
    )

    if fitness_insights:

        all_insights.extend(
            fitness_insights
        )

    # --------------------------------------------------------
    # MEDICATION INSIGHTS
    # --------------------------------------------------------

    medication_insights = generate_medication_insights(
        medication_adherence
    )

    all_insights.extend(
        medication_insights
    )

    # --------------------------------------------------------
    # GOAL INSIGHTS
    # --------------------------------------------------------

    if fitness_data:

        latest_record = fitness_data[-1]

        steps = latest_record[1]
        calories = latest_record[2]
        water = latest_record[3]

        goal_insights = generate_goal_insights(
            steps,
            steps_goal,
            water,
            water_goal,
            calories,
            calories_goal
        )

        all_insights.extend(
            goal_insights
        )

    return all_insights


# ============================================================
# STEPS CHART
# ============================================================

def create_fitness_chart(fitness_data):

    if not fitness_data:
        return None

    df = pd.DataFrame(
        fitness_data,
        columns=["ID", "Steps", "Calories", "Water"]
    )

    fig, ax = plt.subplots()

    ax.plot(
        range(1, len(df) + 1),
        df["Steps"],
        marker="o"
    )

    ax.set_title("Steps Progress")
    ax.set_xlabel("Fitness Record")
    ax.set_ylabel("Steps")

    ax.grid(True)

    return fig


# ============================================================
# CALORIES CHART
# ============================================================

def create_calories_chart(fitness_data):

    if not fitness_data:
        return None

    df = pd.DataFrame(
        fitness_data,
        columns=["ID", "Steps", "Calories", "Water"]
    )

    fig, ax = plt.subplots()

    ax.plot(
        range(1, len(df) + 1),
        df["Calories"],
        marker="o"
    )

    ax.set_title("Calories Burned Progress")
    ax.set_xlabel("Fitness Record")
    ax.set_ylabel("Calories")

    ax.grid(True)

    return fig


# ============================================================
# WATER INTAKE CHART
# ============================================================

def create_water_chart(fitness_data):

    if not fitness_data:
        return None

    df = pd.DataFrame(
        fitness_data,
        columns=["ID", "Steps", "Calories", "Water"]
    )

    fig, ax = plt.subplots()

    ax.plot(
        range(1, len(df) + 1),
        df["Water"],
        marker="o"
    )

    ax.set_title("Water Intake Progress")
    ax.set_xlabel("Fitness Record")
    ax.set_ylabel("Water Intake (Liters)")

    ax.grid(True)

    return fig