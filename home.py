
import streamlit as st
import re

from health_assessment import (
    assess_symptoms,
    assess_overall_health
)

from medicine import (
    view_medicines,
    calculate_adherence
)

from caregiver import (
    view_caregivers
)

from health_api import (
    get_steps,
    get_calories,
    get_water
)

from database import (
    view_fitness
)

from health_analysis import (
    analyze_fitness_data
)

from health_goals import (
    get_health_goal_progress,
    get_goal_status
)

from health_report import (
    generate_health_report
)


# ============================================================
# CLEAN OUTPUT
# ============================================================

def clean_ai_output(text):

    if not text:
        return ""

    text = str(text)

    # Remove localhost markdown links
    text = re.sub(
        r'\[([^\]]+)\]\(http://localhost[^)]*\)',
        r'\1',
        text
    )

    # Remove HTML tags
    text = re.sub(
        r'<[^>]+>',
        '',
        text
    )

    # Remove duplicate heading
    text = text.replace(
        "AI Health Assessment",
        ""
    )

    text = text.replace(
        "### AI Health Assessment",
        ""
    )

    return text.strip()


# ============================================================
# WELLNESS SCORE
# ============================================================

def calculate_wellness_score(
    steps,
    calories,
    water,
    adherence
):
    """
    Calculates a simple non-medical wellness score.
    """

    try:

        steps_score = min(
            (steps / 10000) * 100,
            100
        )

        calories_score = min(
            (calories / 500) * 100,
            100
        )

        water_score = min(
            (water / 3) * 100,
            100
        )

        adherence_score = min(
            adherence,
            100
        )

        score = (
            steps_score * 0.25
            + calories_score * 0.20
            + water_score * 0.25
            + adherence_score * 0.30
        )

        return round(score)

    except Exception:
        return 0


# ============================================================
# HEALTH STATUS
# ============================================================

def get_health_status(score):

    if score < 20:
        return "😟", "Needs Attention"

    elif score < 40:
        return "😐", "Getting Started"

    elif score < 60:
        return "🙂", "Fair"

    elif score < 80:
        return "😊", "Good"

    else:
        return "💪", "Excellent"


# ============================================================
# HOME PAGE
# ============================================================

def home_page():

    st.title(
        "🏠 Health Monitoring Dashboard"
    )

    st.caption(
        "Track your health, understand your symptoms, "
        "and monitor your daily wellness."
    )

    # ========================================================
    # SESSION STATE
    # ========================================================

    if "home_section" not in st.session_state:
        st.session_state["home_section"] = None

    if "symptom_result" not in st.session_state:
        st.session_state["symptom_result"] = None

    if "overall_result" not in st.session_state:
        st.session_state["overall_result"] = None

    # ========================================================
    # MAIN OPTIONS
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "🩺 What are you feeling?"
        )

        st.write(
            "Describe your symptoms and get general health guidance."
        )

        if st.button(
            "🔍 Check My Symptoms",
            use_container_width=True
        ):

            st.session_state["home_section"] = "feeling"

            st.session_state["overall_result"] = None

    with col2:

        st.subheader(
            "💚 How is your health?"
        )

        st.write(
            "View your fitness, medication, goals, "
            "and overall health progress."
        )

        if st.button(
            "📊 Open Your Health",
            use_container_width=True
        ):

            st.session_state["home_section"] = "health"

            st.session_state["symptom_result"] = None

    st.divider()

    # ========================================================
    # DEFAULT MESSAGE
    # ========================================================

    if st.session_state["home_section"] is None:

        st.info(
            "👆 Choose an option above to check your symptoms "
            "or view your health."
        )

    # ========================================================
    # SYMPTOM SECTION
    # ========================================================

    if st.session_state["home_section"] == "feeling":

        st.header(
            "🩺 Symptom Assessment"
        )

        symptoms = st.text_area(
            "Describe what you are feeling:",
            placeholder=(
                "Example: I have headache, mild fever and tiredness..."
            ),
            height=150,
            key="symptoms_input"
        )

        if st.button(
            "🔍 Analyze My Symptoms",
            use_container_width=True
        ):

            if not symptoms.strip():

                st.warning(
                    "⚠️ Please describe your symptoms first."
                )

            else:

                with st.spinner(
                    "🔎 Checking your symptoms..."
                ):

                    try:

                        result = assess_symptoms(
                            symptoms
                        )

                        st.session_state[
                            "symptom_result"
                        ] = clean_ai_output(
                            result
                        )

                    except Exception as e:

                        st.error(
                            f"Unable to analyze symptoms: {e}"
                        )

        # ----------------------------------------------------
        # DISPLAY RESULT
        # ----------------------------------------------------

        if st.session_state.get(
            "symptom_result"
        ):

            st.divider()

            st.subheader(
                "🧠 Health Assessment"
            )

            st.markdown(
                st.session_state[
                    "symptom_result"
                ]
            )

            st.warning(
                "⚠️ This assessment provides general health "
                "information only. It is not a medical diagnosis "
                "and does not replace professional medical advice."
            )

    # ========================================================
    # HEALTH SECTION
    # ========================================================

    if st.session_state["home_section"] == "health":

        st.header(
            "💚 Your Health Overview"
        )

        # ----------------------------------------------------
        # GET HEALTH DATA
        # ----------------------------------------------------

        try:
            steps = get_steps()
        except Exception:
            steps = 0

        try:
            calories = get_calories()
        except Exception:
            calories = 0

        try:
            water = get_water()
        except Exception:
            water = 0

        try:
            fitness_data = view_fitness()
        except Exception:
            fitness_data = []

        try:
            medicines = view_medicines()
        except Exception:
            medicines = []

        try:
            adherence = calculate_adherence()
        except Exception:
            adherence = 0

        # ----------------------------------------------------
        # WELLNESS SCORE
        # ----------------------------------------------------

        wellness_score = calculate_wellness_score(
            steps,
            calories,
            water,
            adherence
        )

        emoji, status = get_health_status(
            wellness_score
        )

        st.subheader(
            "🌟 Wellness Score"
        )

        score_col1, score_col2 = st.columns(
            [1, 3]
        )

        with score_col1:

            st.metric(
                "Wellness",
                f"{wellness_score}%"
            )

        with score_col2:

            st.write(
                f"### {emoji} {status}"
            )

            st.progress(
                wellness_score / 100
            )

        # ====================================================
        # HEALTH JOURNEY
        # ====================================================

        st.subheader(
            "🛤️ Health Journey"
        )

        journey_cols = st.columns(5)

        journey_labels = [
            "🌱 Started",
            "🚶 Active",
            "💧 Hydrated",
            "💊 Consistent",
            "🏆 Healthy"
        ]

        for col, label in zip(
            journey_cols,
            journey_labels
        ):

            with col:
                st.write(label)

        # ====================================================
        # TODAY'S SUMMARY
        # ====================================================

        st.subheader(
            "📊 Today's Summary"
        )

        metric1, metric2, metric3, metric4 = st.columns(4)

        with metric1:

            st.metric(
                "🚶 Steps",
                f"{steps:,}"
            )

        with metric2:

            st.metric(
                "🔥 Calories",
                f"{calories}"
            )

        with metric3:

            st.metric(
                "💧 Water",
                f"{water} L"
            )

        with metric4:

            st.metric(
                "💊 Adherence",
                f"{adherence:.0f}%"
            )

        # ====================================================
        # DAILY GOALS
        # ====================================================

        st.subheader(
            "🎯 Daily Goals"
        )

        # Steps

        st.write(
            "🚶 Steps Goal — 10,000"
        )

        steps_progress = min(
            steps / 10000,
            1.0
        )

        st.progress(
            steps_progress
        )

        st.caption(
            f"{steps:,} / 10,000 steps"
        )

        # Water

        st.write(
            "💧 Water Goal — 3 L"
        )

        water_progress = min(
            water / 3,
            1.0
        )

        st.progress(
            water_progress
        )

        st.caption(
            f"{water} / 3 L"
        )

        # Calories

        st.write(
            "🔥 Calories Goal — 500"
        )

        calories_progress = min(
            calories / 500,
            1.0
        )

        st.progress(
            calories_progress
        )

        st.caption(
            f"{calories} / 500 calories"
        )

        # ====================================================
        # HEALTH GOAL ANALYTICS
        # ====================================================

        st.subheader(
            "🎯 Health Goal Progress"
        )

        try:

            goal_progress = (
                get_health_goal_progress()
            )

            if goal_progress:
                st.write(goal_progress)

        except Exception:

            st.info(
                "Health goal progress is currently unavailable."
            )

        try:

            goal_status = (
                get_goal_status()
            )

            if goal_status:
                st.write(goal_status)

        except Exception:
            pass

        # ====================================================
        # HEALTH INSIGHTS
        # ====================================================

        st.subheader(
            "💡 Health Insights"
        )

        try:

            insights = analyze_fitness_data(
                fitness_data
            )

            if insights:

                st.write(
                    insights
                )

            else:

                st.info(
                    "Not enough fitness data available for insights."
                )

        except Exception:

            st.info(
                "Health insights are currently unavailable."
            )

        # ====================================================
        # MEDICATIONS
        # ====================================================

        st.subheader(
            "💊 Medications"
        )

        if medicines:

            try:

                for medicine in medicines:

                    if isinstance(
                        medicine,
                        dict
                    ):

                        name = medicine.get(
                            "name",
                            "Medicine"
                        )

                        dosage = medicine.get(
                            "dosage",
                            ""
                        )

                        st.write(
                            f"💊 **{name}** {dosage}"
                        )

                    else:

                        st.write(
                            f"💊 {medicine}"
                        )

            except Exception:

                st.write(
                    medicines
                )

        else:

            st.info(
                "No medications added yet."
            )

        st.write(
            f"💊 Medication Adherence: "
            f"**{adherence:.0f}%**"
        )

        # ====================================================
        # FAMILY & CAREGIVER
        # ====================================================

        st.subheader(
            "👨‍👩‍👧 Family & Caregiver"
        )

        try:

            caregivers = view_caregivers()

            if caregivers:

                for caregiver in caregivers:

                    if isinstance(
                        caregiver,
                        dict
                    ):

                        name = caregiver.get(
                            "name",
                            "Caregiver"
                        )

                        relation = caregiver.get(
                            "relation",
                            ""
                        )

                        st.write(
                            f"👤 **{name}** {relation}"
                        )

                    else:

                        st.write(
                            f"👤 {caregiver}"
                        )

            else:

                st.info(
                    "No caregivers added yet."
                )

        except Exception:

            st.info(
                "Caregiver information is currently unavailable."
            )

        # ====================================================
        # HEALTH REPORT
        # ====================================================

        st.subheader(
            "📄 Health Report"
        )

        if st.button(
            "📥 Generate Health Report",
            use_container_width=True
        ):

            try:

                report = generate_health_report()

                if report:

                    st.download_button(
                        label="⬇️ Download Health Report",
                        data=report,
                        file_name="health_report.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                else:

                    st.warning(
                        "Unable to generate the health report."
                    )

            except Exception as e:

                st.error(
                    f"Unable to generate health report: {e}"
                )

        # ====================================================
        # OVERALL HEALTH
        # ====================================================

        st.subheader(
            "🧠 Overall Health Analysis"
        )

        st.write(
            "Get a health summary based on your available "
            "fitness, hydration, calorie, and medication data."
        )

        if st.button(
            "🧠 Analyze My Overall Health",
            use_container_width=True
        ):

            with st.spinner(
                "🔎 Preparing your health analysis..."
            ):

                try:

                    result = assess_overall_health()

                    st.session_state[
                        "overall_result"
                    ] = clean_ai_output(
                        result
                    )

                except Exception as e:

                    st.error(
                        f"Unable to generate overall health analysis: {e}"
                    )

        if st.session_state.get(
            "overall_result"
        ):

            st.divider()

            st.subheader(
                "🧠 Overall Health Assessment"
            )

            st.markdown(
                st.session_state[
                    "overall_result"
                ]
            )

            st.warning(
                "⚠️ This analysis is for general wellness "
                "information only and does not replace "
                "professional medical advice."
            )

    # ========================================================
    # FOOTER
    # ========================================================

    st.divider()

    st.caption(
        "⚕️ Personal Health Assistant | "
        "No external AI API required | "
        "For informational purposes only. "
        "Always consult a qualified healthcare professional "
        "for medical decisions."
    )
