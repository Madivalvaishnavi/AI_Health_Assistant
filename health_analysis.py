import pandas as pd
import matplotlib.pyplot as plt


def analyze_fitness_data(fitness_data):
    """
    Analyzes fitness data and returns basic health insights.
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

    # Basic insights
    if average_steps < 5000:
        insights.append(
            "Your average step count is low. Try to include more walking in your daily routine."
        )
    else:
        insights.append(
            "Your average step count is good. Keep staying active!"
        )

    if average_water < 2:
        insights.append(
            "Your average water intake is below 2 liters. Remember to stay hydrated."
        )
    else:
        insights.append(
            "Your water intake looks good. Keep staying hydrated!"
        )

    return {
        "average_steps": round(average_steps, 2),
        "average_calories": round(average_calories, 2),
        "average_water": round(average_water, 2)
    }, insights


def create_fitness_chart(fitness_data):

    if not fitness_data:
        return None

    df = pd.DataFrame(
        fitness_data,
        columns=["ID", "Steps", "Calories", "Water"]
    )

    # Create chart
    fig, ax = plt.subplots()

    ax.plot(
        range(1, len(df) + 1),
        df["Steps"],
        marker="o"
    )

    ax.set_title("Steps Progress")
    ax.set_xlabel("Fitness Record")
    ax.set_ylabel("Steps")

    return fig