# ============================================================
# HEALTH GOALS
# ============================================================


# ============================================================
# CALCULATE PROGRESS
# ============================================================

def calculate_progress(current, goal):

    if goal <= 0:
        return 0

    progress = (current / goal) * 100

    # Maximum progress is 100%
    if progress > 100:
        progress = 100

    return round(progress, 2)


# ============================================================
# GET GOAL STATUS
# ============================================================

def get_goal_status(current, goal):

    if goal <= 0:
        return "⚪ Invalid Goal"

    if current >= goal:
        return "🟢 Goal Completed"

    progress = (current / goal) * 100

    if progress >= 70:
        return "🟡 Almost There"

    if progress >= 40:
        return "🟠 In Progress"

    return "🔴 Needs Improvement"


# ============================================================
# GET REMAINING VALUE
# ============================================================

def get_remaining(current, goal):

    remaining = goal - current

    if remaining <= 0:
        return 0

    return round(remaining, 2)


# ============================================================
# GET HEALTH GOAL PROGRESS
# ============================================================

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


# ============================================================
# GET COMPLETE GOAL ANALYTICS
# ============================================================

def get_goal_analytics(
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


    # --------------------------------------------------------
    # OVERALL WELLNESS PROGRESS
    # --------------------------------------------------------

    overall_progress = (
        steps_progress
        + water_progress
        + calories_progress
    ) / 3


    return {

        "steps": {
            "current": steps,
            "goal": steps_goal,
            "progress": steps_progress,
            "remaining": get_remaining(
                steps,
                steps_goal
            ),
            "status": get_goal_status(
                steps,
                steps_goal
            )
        },

        "water": {
            "current": water,
            "goal": water_goal,
            "progress": water_progress,
            "remaining": get_remaining(
                water,
                water_goal
            ),
            "status": get_goal_status(
                water,
                water_goal
            )
        },

        "calories": {
            "current": calories,
            "goal": calories_goal,
            "progress": calories_progress,
            "remaining": get_remaining(
                calories,
                calories_goal
            ),
            "status": get_goal_status(
                calories,
                calories_goal
            )
        },

        "overall": round(
            overall_progress,
            2
        )
    }