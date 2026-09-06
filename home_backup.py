import streamlit as st

# ============================================================
# AI HEALTH ASSESSMENT
# ============================================================

from health_assessment import (
    assess_symptoms,
    assess_overall_health
)


# ============================================================
# EXISTING PROJECT IMPORTS
# ============================================================

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
# PAGE STYLE
# ============================================================

def apply_home_style():

    st.markdown(
        """
        <style>

        /* Main page */
        .main {
            padding-top: 1rem;
        }

        /* Hide unnecessary anchor text */
        h1 a, h2 a, h3 a {
            display: none !important;
        }

        /* Hero section */
        .home-hero {
            padding: 24px 10px 20px 10px;
            text-align: center;
        }

        .home-hero h1 {
            font-size: 38px;
            margin-bottom: 6px;
        }

        .home-hero p {
            font-size: 17px;
            color: #666;
            margin-top: 0;
        }

        /* Feature cards */
        .feature-card {
            border: 1px solid rgba(128,128,128,0.25);
            border-radius: 16px;
            padding: 22px;
            min-height: 150px;
            background: rgba(128,128,128,0.04);
        }

        .feature-card h3 {
            margin-top: 0;
            margin-bottom: 8px;
        }

        .feature-card p {
            color: #666;
            margin-bottom: 0;
        }

        /* Health journey */
        .health-journey {
            border: 1px solid rgba(128,128,128,0.25);
            border-radius: 18px;
            padding: 24px;
            text-align: center;
            background: rgba(128,128,128,0.04);
        }

        .journey-emojis {
            font-size: 31px;
            letter-spacing: 12px;
            margin: 14px 0;
        }

        .journey-labels {
            display: flex;
            justify-content: space-around;
            color: #777;
            font-size: 13px;
        }

        .health-status {
            font-size: 21px;
            font-weight: 600;
            margin-top: 12px;
        }

        /* Metric cards */
        div[data-testid="stMetric"] {
            border: 1px solid rgba(128,128,128,0.20);
            border-radius: 14px;
            padding: 12px;
        }

        /* Section spacing */
        .section-space {
            margin-top: 10px;
            margin-bottom: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HEALTH SCORE
# ============================================================

def calculate_wellness_score(
    steps,
    calories,
    water,
    adherence,
    steps_goal=10000,
    calories_goal=500,
    water_goal=3
):
    """
    Calculates a simple wellness/progress score.

    This is NOT a medical score.
    It only reflects tracked application data.
    """

    try:
        steps_score = min(
            float(steps) / float(steps_goal),
            1
        )

        calories_score = min(
            float(calories) / float(calories_goal),
            1
        )

        water_score = min(
            float(water) / float(water_goal),
            1
        )

        adherence_score = min(
            float(adherence) / 100,
            1
        )

        score = (
            steps_score * 25
            + calories_score * 25
            + water_score * 25
            + adherence_score * 25
        )

        return round(score)

    except Exception:
        return 0


# ============================================================
# HEALTH STATUS
# ============================================================

def get_health_status(score):

    if score < 20:
        return (
            "😟",
            "Needs Attention",
            "Try to focus on your basic daily health goals."
        )

    elif score < 40:
        return (
            "😐",
            "Getting Started",
            "You're making progress. Keep building healthy habits."
        )

    elif score < 60:
        return (
            "🙂",
            "Fair",
            "You're on the right track. Keep improving consistently."
        )

    elif score < 80:
        return (
            "😊",
            "Good",
            "Great progress! Keep maintaining your healthy routine."
        )

    else:
        return (
            "💪",
            "Excellent",
            "Excellent progress! Keep maintaining your healthy habits."
        )


# ============================================================
# HEALTH JOURNEY UI
# ============================================================

def display_health_journey(score):

    emoji, status, message = get_health_status(score)

    st.markdown(
        f"""
        <div class="health-journey">

            <h3>💚 Your Health Journey</h3>

            <p>
                Your wellness progress based on the information
                tracked in this application.
            </p>

            <div class="journey-emojis">
                😟　😐　🙂　😊　💪
            </div>

            <div class="journey-labels">
                <span>Needs Attention</span>
                <span>Getting Started</span>
                <span>Fair</span>
                <span>Good</span>
                <span>Excellent</span>
            </div>

            <div class="health-status">
                {emoji} {status}
            </div>

            <p>{message}</p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(
        min(score, 100) / 100
    )

    st.caption(
        f"Wellness progress: {score}% "
        "• This is a lifestyle/progress indicator, not a medical diagnosis."
    )


# ============================================================
# HOME PAGE
# ============================================================

def home_page():

    apply_home_style()

    # ========================================================
    # HERO
    # ========================================================

    st.markdown(
        """
        <div class="home-hero">

            <h1>🏠 Health Monitoring Dashboard</h1>

            <p>
                Your personal health companion for tracking,
                understanding and improving your daily wellness.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()


    # ========================================================
    # TWO MAIN OPTIONS
    # ========================================================

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # WHAT ARE YOU FEELING?
    # --------------------------------------------------------

    with col1:

        st.markdown(
            """
            <div class="feature-card">

                <h3>🩺 What are you feeling?</h3>

                <p>
                    Describe your symptoms naturally and get
                    general AI-powered health guidance.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        if st.button(
            "🩺 Check My Symptoms",
            use_container_width=True,
            type="primary"
        ):

            st.session_state["home_section"] = "feeling"

            st.session_state.pop(
                "overall_health_result",
                None
            )


    # --------------------------------------------------------
    # HOW IS YOUR HEALTH?
    # --------------------------------------------------------

    with col2:

        st.markdown(
            """
            <div class="feature-card">

                <h3>💚 How is your health?</h3>

                <p>
                    View your fitness, medication, goals and
                    overall wellness progress.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        if st.button(
            "💚 Open Your Health",
            use_container_width=True
        ):

            st.session_state["home_section"] = "health"

            st.session_state.pop(
                "symptom_result",
                None
            )


    # ========================================================
    # DEFAULT MESSAGE
    # ========================================================

    if "home_section" not in st.session_state:

        st.divider()

        st.info(
            "👆 Choose an option above to get started."
        )

        return


    # ========================================================
    # 🩺 WHAT ARE YOU FEELING?
    # ========================================================

    if st.session_state["home_section"] == "feeling":

        st.divider()

        st.subheader(
            "🩺 What are you feeling?"
        )

        st.write(
            "Tell us what you are experiencing in your own words."
        )

        symptoms = st.text_area(
            "Describe your symptoms",
            placeholder=(
                "Example: I have headache and fever "
                "since yesterday..."
            ),
            height=120,
            key="symptoms_input"
        )

        st.caption(
            "You don't need medical terms. Just describe "
            "what you are feeling naturally."
        )


        # ----------------------------------------------------
        # ANALYZE
        # ----------------------------------------------------

        if st.button(
            "🔍 Analyze My Symptoms",
            use_container_width=True,
            type="primary"
        ):

            if not symptoms.strip():

                st.warning(
                    "Please tell us what you are feeling."
                )

            else:

                with st.spinner(
                    "🧠 AI is analyzing your symptoms..."
                ):

                    try:

                        result = assess_symptoms(
                            symptoms
                        )

                        st.session_state[
                            "symptom_result"
                        ] = result

                    except Exception as e:

                        st.error(
                            f"Unable to analyze symptoms: {e}"
                        )


        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        if "symptom_result" in st.session_state:

            st.divider()

            st.subheader(
                "🧠 AI Health Assessment"
            )

            with st.container(border=True):

                st.markdown(
                    st.session_state[
                        "symptom_result"
                    ]
                )

            st.warning(
                "⚠️ This assessment provides general health "
                "guidance only. It is not a medical diagnosis "
                "and does not replace professional medical care."
            )


    # ========================================================
    # 💚 HOW IS YOUR HEALTH?
    # ========================================================

    elif st.session_state["home_section"] == "health":

        st.divider()

        st.subheader(
            "💚 Your Health"
        )

        st.write(
            "A quick overview of your tracked health and "
            "wellness information."
        )


        # ====================================================
        # GET DATA
        # ====================================================

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


        # ====================================================
        # ADHERENCE
        # ====================================================

        try:
            adherence = calculate_adherence()
        except Exception:
            adherence = 0


        # ====================================================
        # WELLNESS JOURNEY
        # ====================================================

        wellness_score = calculate_wellness_score(
            steps,
            calories,
            water,
            adherence
        )

        display_health_journey(
            wellness_score
        )


        st.divider()


        # ====================================================
        # TODAY'S SUMMARY
        # ====================================================

        st.subheader(
            "📊 Today's Health Summary"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "👣 Steps",
                steps
            )

        with col2:

            st.metric(
                "🔥 Calories",
                calories
            )

        with col3:

            st.metric(
                "💧 Water",
                f"{water} L"
            )

        with col4:

            st.metric(
                "💊 Medicines",
                len(medicines)
            )


        st.divider()


        # ====================================================
        # DAILY HEALTH GOALS
        # ====================================================

        st.subheader(
            "🎯 Daily Health Goals"
        )

        steps_goal = 10000
        water_goal = 3
        calories_goal = 500

        try:

            progress = get_health_goal_progress(
                steps,
                steps_goal,
                water,
                water_goal,
                calories,
                calories_goal
            )

        except Exception:

            progress = {
                "steps": 0,
                "water": 0,
                "calories": 0
            }


        col1, col2, col3 = st.columns(3)


        with col1:

            st.write("👣 Steps Goal")

            st.progress(
                min(
                    float(progress["steps"]),
                    100
                ) / 100
            )

            st.write(
                f"{float(progress['steps']):.1f}% completed"
            )

            st.caption(
                get_goal_status(
                    steps,
                    steps_goal
                )
            )


        with col2:

            st.write("💧 Water Goal")

            st.progress(
                min(
                    float(progress["water"]),
                    100
                ) / 100
            )

            st.write(
                f"{float(progress['water']):.1f}% completed"
            )

            st.caption(
                get_goal_status(
                    water,
                    water_goal
                )
            )


        with col3:

            st.write("🔥 Calories Goal")

            st.progress(
                min(
                    float(progress["calories"]),
                    100
                ) / 100
            )

            st.write(
                f"{float(progress['calories']):.1f}% completed"
            )

            st.caption(
                get_goal_status(
                    calories,
                    calories_goal
                )
            )


        st.divider()


        # ====================================================
        # HEALTH INSIGHTS
        # ====================================================

        st.subheader(
            "💡 Health Insights"
        )

        if fitness_data:

            try:

                analysis, insights = analyze_fitness_data(
                    fitness_data
                )

                if insights:

                    for insight in insights:

                        st.info(insight)

                else:

                    st.info(
                        "No additional insights available."
                    )

            except Exception:

                st.info(
                    "Unable to generate health insights."
                )

        else:

            st.info(
                "Add fitness data to receive health insights."
            )


        st.divider()


        # ====================================================
        # MEDICATION SUMMARY
        # ====================================================

        st.subheader(
            "💊 Medication Summary"
        )

        if medicines:

            st.write(
                f"You currently have "
                f"**{len(medicines)} medicine(s)** saved."
            )

            for medicine in medicines:

                try:

                    st.write(
                        f"💊 {medicine[1]} | "
                        f"Dosage: {medicine[2]} | "
                        f"Time: {medicine[3]}"
                    )

                except Exception:

                    st.write(
                        f"💊 {medicine}"
                    )

        else:

            st.info(
                "No medicines have been saved yet."
            )


        st.divider()


        # ====================================================
        # MEDICATION ADHERENCE
        # ====================================================

        st.subheader(
            "💊 Medication Adherence"
        )

        st.metric(
            "Today's Medication Adherence",
            f"{float(adherence):.1f}%"
        )


        st.divider()


        # ====================================================
        # FAMILY & CAREGIVER
        # ====================================================

        st.subheader(
            "👨‍👩‍👧 Family & Caregiver"
        )

        try:

            caregivers = view_caregivers()

        except Exception:

            caregivers = []


        if caregivers:

            st.write(
                f"**{len(caregivers)} caregiver(s)** registered."
            )

            for caregiver in caregivers:

                try:

                    st.write(
                        f"👤 {caregiver[1]} | "
                        f"📞 {caregiver[2]}"
                    )

                except Exception:

                    st.write(
                        f"👤 {caregiver}"
                    )

        else:

            st.info(
                "No caregiver has been added yet."
            )


        st.divider()


        # ====================================================
        # HEALTH REPORT
        # ====================================================

        st.subheader(
            "📄 Health Report"
        )

        if fitness_data:

            try:

                report = generate_health_report(
                    fitness_data,
                    medicines
                )

                st.download_button(
                    label="📥 Download Health Report",
                    data=report,
                    file_name="health_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            except Exception:

                st.error(
                    "Unable to generate the health report."
                )

        else:

            st.info(
                "Add fitness data to generate your health report."
            )


        st.divider()


        # ====================================================
        # AI OVERALL HEALTH
        # ====================================================

        st.subheader(
            "🧠 AI Overall Health Assessment"
        )

        st.write(
            "Get an AI-based overview using the health "
            "information tracked in this application."
        )

        if st.button(
            "📊 Check My Overall Health",
            use_container_width=True,
            type="primary"
        ):

            with st.spinner(
                "🧠 AI is reviewing your health data..."
            ):

                try:

                    result = assess_overall_health()

                    st.session_state[
                        "overall_health_result"
                    ] = result

                except Exception as e:

                    st.error(
                        f"Unable to generate assessment: {e}"
                    )


        if "overall_health_result" in st.session_state:

            st.divider()

            with st.container(border=True):

                st.markdown(
                    st.session_state[
                        "overall_health_result"
                    ]
                )

            st.warning(
                "⚠️ This is an AI-generated health overview "
                "and not a medical diagnosis."
            )


        # ====================================================
        # FOOTER
        # ====================================================

        st.divider()

        st.caption(
            "🩺 AI Personal Health Assistant provides general "
            "health guidance and wellness monitoring support. "
            "It does not replace professional medical care."
        )