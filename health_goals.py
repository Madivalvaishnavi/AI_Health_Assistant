# ============================================================
# HEALTH GOALS
# ============================================================

def calculate_progress(current, goal):

    if goal <= 0:
        return 0

    progress = (current / goal) * 100

    # Maximum progress shown is 100%
    if progress > 100:
        progress = 100

    return progress


def get_goal_status(current, goal):

    if current >= goal:
        return "🎉 Goal Completed!"

    remaining = goal - current

    return f"Keep going! {remaining} more to reach your goal."


def get_health_goal_progress(
    steps,
    steps_goal,
    water,
    water_goal,
    calories,
    calories_goal
):

    steps_progress = calculate_progress(
        steps,
        steps_goal
    )

    water_progress = calculate_progress(
        water,
        water_goal
    )

    calories_progress = calculate_progress(
        calories,
        calories_goal
    )

    return {
        "steps": steps_progress,
        "water": water_progress,
        "calories": calories_progress
    }