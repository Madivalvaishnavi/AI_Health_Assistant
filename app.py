import streamlit as st

from medicine import add_medicine, view_medicines
from health_chatbot import health_chatbot
from health_api import get_steps, get_calories, get_water
from user import register_user, login_user

from database import view_fitness
from health_analysis import analyze_fitness_data, create_fitness_chart

from medication_interaction import check_medication_interaction
from health_report import generate_health_report

# Health Data Import / Export
from health_data_formats import (
    export_json,
    export_csv,
    export_xml,
    import_json,
    import_csv,
    import_xml
)

# Health Goals
from health_goals import (
    calculate_progress,
    get_goal_status,
    get_health_goal_progress
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🩺"
)

st.title("🩺 AI Personal Health Assistant")
st.write("Welcome to your AI Health Assistant!")


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Register"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ============================================================
# LOGIN / REGISTER
# ============================================================

if not st.session_state.logged_in:

    # ========================================================
    # REGISTER
    # ========================================================

    if st.session_state.page == "Register":

        st.header("👤 User Registration")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Register"):

            if username and password:

                if register_user(
                    username,
                    password
                ):

                    st.success(
                        "Registration Successful! Please Login."
                    )

                    st.session_state.page = "Login"

                    st.rerun()

                else:

                    st.error(
                        "Username already exists!"
                    )

            else:

                st.warning(
                    "Please enter username and password."
                )

        if st.button("Go to login"):

            st.session_state.page = "Login"

            st.rerun()


    # ========================================================
    # LOGIN
    # ========================================================

    elif st.session_state.page == "Login":

        st.header("🔐 User Login")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            user = login_user(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True

                st.success(
                    "Login Successful!"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

        if st.button("Go to Register"):

            st.session_state.page = "Register"

            st.rerun()

    st.stop()


# ============================================================
# SIDEBAR MENU
# ============================================================

menu = st.sidebar.selectbox(
    "Choose Option",
    [
        "Home",
        "Medication Tracker",
        "Fitness Tracker",
        "Health Goals",
        "Medication Interaction Checker",
        "Health Report",
        "Health Data Import/Export",
        "Health Chatbot",
        "Logout"
    ]
)


# ============================================================
# HOME
# ============================================================

if menu == "Home":

    st.header("🏠 Dashboard")

    st.write(
        "Welcome to AI Personal Health Assistant!"
    )

    st.info(
        "Use the sidebar to track your medication, "
        "monitor fitness data, set health goals, "
        "check medication interactions, "
        "generate health reports, "
        "import/export health data, "
        "and ask the AI Health Chatbot questions."
    )


# ============================================================
# MEDICATION TRACKER
# ============================================================

elif menu == "Medication Tracker":

    st.header("💊 Medication Tracker")

    medicine_name = st.text_input(
        "Medicine Name"
    )

    dosage = st.text_input(
        "Dosage"
    )

    time = st.text_input(
        "Time"
    )

    if st.button("Save Medicine"):

        if medicine_name and dosage and time:

            add_medicine(
                medicine_name,
                dosage,
                time
            )

            st.success(
                "Medicine Saved Successfully!"
            )

            st.rerun()

        else:

            st.warning(
                "Please enter medicine name, dosage, and time."
            )


    st.subheader(
        "📋 Saved Medicines"
    )

    medicines = view_medicines()

    if medicines:

        for medicine in medicines:

            st.write(
                medicine
            )

    else:

        st.info(
            "No medicines saved yet."
        )


# ============================================================
# FITNESS TRACKER
# ============================================================

elif menu == "Fitness Tracker":

    st.header("🏃 Fitness Tracker")


    # ========================================================
    # ENTER FITNESS DATA
    # ========================================================

    st.subheader(
        "📝 Enter Your Fitness Data"
    )

    steps_input = st.number_input(
        "👣 Steps",
        min_value=0,
        step=100
    )

    calories_input = st.number_input(
        "🔥 Calories Burned",
        min_value=0,
        step=10
    )

    water_input = st.number_input(
        "💧 Water Intake (Liters)",
        min_value=0.0,
        step=0.1
    )


    # ========================================================
    # SAVE FITNESS DATA
    # ========================================================

    if st.button("Save Fitness Data"):

        import sqlite3

        connection = sqlite3.connect(
            "health.db"
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO fitness
            (steps, calories, water)
            VALUES (?, ?, ?)
            """,
            (
                steps_input,
                calories_input,
                water_input
            )
        )

        connection.commit()

        connection.close()

        st.success(
            "Fitness data saved successfully!"
        )

        st.rerun()


    # ========================================================
    # CURRENT FITNESS VALUES
    # ========================================================

    st.subheader(
        "📊 Current Fitness Data"
    )

    st.write(
        "👣 Steps:",
        get_steps()
    )

    st.write(
        "🔥 Calories:",
        get_calories()
    )

    st.write(
        "💧 Water Intake:",
        get_water(),
        "L"
    )


    # ========================================================
    # FITNESS RECORDS
    # ========================================================

    fitness_data = view_fitness()


    # ========================================================
    # HEALTH DATA ANALYSIS
    # ========================================================

    st.subheader(
        "📈 Health Data Analysis"
    )

    if fitness_data:

        analysis, insights = analyze_fitness_data(
            fitness_data
        )


        # ====================================================
        # AVERAGE VALUES
        # ====================================================

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Average Steps",
                analysis["average_steps"]
            )

        with col2:

            st.metric(
                "Average Calories",
                analysis["average_calories"]
            )

        with col3:

            st.metric(
                "Average Water",
                f"{analysis['average_water']} L"
            )


        # ====================================================
        # HEALTH INSIGHTS
        # ====================================================

        st.subheader(
            "💡 Health Insights"
        )

        for insight in insights:

            st.info(
                insight
            )


        # ====================================================
        # VISUALIZATION
        # ====================================================

        st.subheader(
            "📊 Steps Progress"
        )

        chart = create_fitness_chart(
            fitness_data
        )

        if chart:

            st.pyplot(
                chart
            )


        # ====================================================
        # SAVED RECORDS
        # ====================================================

        st.subheader(
            "📋 Saved Fitness Records"
        )

        for record in fitness_data:

            st.write(
                record
            )

    else:

        st.info(
            "No fitness records found yet. "
            "Enter your fitness data above and click "
            "'Save Fitness Data' to start your health analysis."
        )


# ============================================================
# HEALTH GOALS
# ============================================================

elif menu == "Health Goals":

    st.header(
        "🎯 Health Goal Setting & Progress Tracking"
    )

    st.write(
        "Set your daily health goals and track your progress."
    )


    # ========================================================
    # SET DAILY GOALS
    # ========================================================

    st.subheader(
        "🎯 Set Your Daily Goals"
    )

    steps_goal = st.number_input(
        "👣 Daily Steps Goal",
        min_value=1,
        value=10000,
        step=500
    )

    water_goal = st.number_input(
        "💧 Daily Water Goal (Liters)",
        min_value=0.1,
        value=3.0,
        step=0.1
    )

    calories_goal = st.number_input(
        "🔥 Daily Calories Goal",
        min_value=1,
        value=500,
        step=50
    )


    # ========================================================
    # SAVE GOALS
    # ========================================================

    if st.button(
        "💾 Save Health Goals"
    ):

        st.session_state.steps_goal = steps_goal

        st.session_state.water_goal = water_goal

        st.session_state.calories_goal = calories_goal

        st.success(
            "Health goals saved successfully!"
        )


    # ========================================================
    # DEFAULT GOALS
    # ========================================================

    if "steps_goal" not in st.session_state:

        st.session_state.steps_goal = steps_goal

    if "water_goal" not in st.session_state:

        st.session_state.water_goal = water_goal

    if "calories_goal" not in st.session_state:

        st.session_state.calories_goal = calories_goal


    # ========================================================
    # GET FITNESS DATA
    # ========================================================

    fitness_data = view_fitness()


    if fitness_data:

        # Get latest fitness record
        latest_record = fitness_data[-1]

        current_steps = latest_record[1]

        current_calories = latest_record[2]

        current_water = latest_record[3]


        # ====================================================
        # CALCULATE GOAL PROGRESS
        # ====================================================

        progress = get_health_goal_progress(

            current_steps,

            st.session_state.steps_goal,

            current_water,

            st.session_state.water_goal,

            current_calories,

            st.session_state.calories_goal

        )


        # ====================================================
        # STEPS PROGRESS
        # ====================================================

        st.subheader(
            "👣 Steps Progress"
        )

        st.write(
            f"**Goal:** {st.session_state.steps_goal:,} steps"
        )

        st.write(
            f"**Current:** {current_steps:,} steps"
        )

        st.write(
            f"**Progress:** {progress['steps']:.1f}%"
        )

        st.progress(
            progress["steps"] / 100
        )

        st.info(
            get_goal_status(
                current_steps,
                st.session_state.steps_goal
            )
        )


        # ====================================================
        # WATER PROGRESS
        # ====================================================

        st.subheader(
            "💧 Water Progress"
        )

        st.write(
            f"**Goal:** {st.session_state.water_goal:.1f} L"
        )

        st.write(
            f"**Current:** {current_water:.1f} L"
        )

        st.write(
            f"**Progress:** {progress['water']:.1f}%"
        )

        st.progress(
            progress["water"] / 100
        )

        st.info(
            get_goal_status(
                current_water,
                st.session_state.water_goal
            )
        )


        # ====================================================
        # CALORIES PROGRESS
        # ====================================================

        st.subheader(
            "🔥 Calories Progress"
        )

        st.write(
            f"**Goal:** {st.session_state.calories_goal:,} calories"
        )

        st.write(
            f"**Current:** {current_calories:,} calories"
        )

        st.write(
            f"**Progress:** {progress['calories']:.1f}%"
        )

        st.progress(
            progress["calories"] / 100
        )

        st.info(
            get_goal_status(
                current_calories,
                st.session_state.calories_goal
            )
        )


    else:

        st.warning(
            "No fitness data available. "
            "Please save your fitness data first."
        )


# ============================================================
# MEDICATION INTERACTION CHECKER
# ============================================================

elif menu == "Medication Interaction Checker":

    st.header(
        "💊 Medication Interaction Checker"
    )

    st.write(
        "Enter two medicine names to check for basic known medication interactions."
    )

    medicine1 = st.text_input(
        "Enter First Medicine"
    )

    medicine2 = st.text_input(
        "Enter Second Medicine"
    )

    if st.button(
        "Check Interaction"
    ):

        if medicine1 and medicine2:

            result = check_medication_interaction(
                medicine1,
                medicine2
            )

            st.warning(
                result
            )

        else:

            st.warning(
                "Please enter both medicine names."
            )


# ============================================================
# HEALTH REPORT
# ============================================================

elif menu == "Health Report":

    st.header(
        "📄 Health Report"
    )

    st.write(
        "Generate a simple summary of your health and fitness data."
    )

    if st.button(
        "Generate Health Report"
    ):

        fitness_data = view_fitness()

        medicines = view_medicines()

        if fitness_data:

            report = generate_health_report(
                fitness_data,
                medicines
            )

            st.subheader(
                "📊 Your Health Summary"
            )

            st.write(
                report
            )

            st.success(
                "Health report generated successfully!"
            )

        else:

            st.warning(
                "No fitness data available. "
                "Please enter fitness data first."
            )


# ============================================================
# HEALTH DATA IMPORT / EXPORT
# ============================================================

elif menu == "Health Data Import/Export":

    st.header(
        "📂 Health Data Import / Export"
    )

    st.write(
        "Export or import your health data using JSON, CSV, and XML formats."
    )


    # ========================================================
    # GET FITNESS DATA
    # ========================================================

    fitness_data = view_fitness()


    # ========================================================
    # EXPORT DATA
    # ========================================================

    st.subheader(
        "📤 Export Health Data"
    )

    export_format = st.selectbox(
        "Choose Export Format",
        [
            "JSON",
            "CSV",
            "XML"
        ]
    )


    if st.button(
        "Prepare Health Data"
    ):

        if fitness_data:

            if export_format == "JSON":

                file_data = export_json(
                    fitness_data
                )

                st.download_button(
                    label="⬇️ Download JSON",
                    data=file_data,
                    file_name="health_data.json",
                    mime="application/json"
                )


            elif export_format == "CSV":

                file_data = export_csv(
                    fitness_data
                )

                st.download_button(
                    label="⬇️ Download CSV",
                    data=file_data,
                    file_name="health_data.csv",
                    mime="text/csv"
                )


            elif export_format == "XML":

                file_data = export_xml(
                    fitness_data
                )

                st.download_button(
                    label="⬇️ Download XML",
                    data=file_data,
                    file_name="health_data.xml",
                    mime="application/xml"
                )

        else:

            st.warning(
                "No health data available to export."
            )


    # ========================================================
    # IMPORT DATA
    # ========================================================

    st.subheader(
        "📥 Import Health Data"
    )

    uploaded_file = st.file_uploader(
        "Upload JSON, CSV, or XML file",
        type=[
            "json",
            "csv",
            "xml"
        ]
    )


    if uploaded_file:

        file_name = uploaded_file.name.lower()

        try:

            if file_name.endswith(
                ".json"
            ):

                imported_data = import_json(
                    uploaded_file
                )


            elif file_name.endswith(
                ".csv"
            ):

                imported_data = import_csv(
                    uploaded_file
                )


            elif file_name.endswith(
                ".xml"
            ):

                imported_data = import_xml(
                    uploaded_file
                )


            else:

                st.error(
                    "Unsupported file format."
                )

                imported_data = None


            if imported_data is not None:

                st.success(
                    "Health data imported successfully!"
                )

                st.subheader(
                    "📋 Imported Health Data"
                )

                st.write(
                    imported_data
                )

        except Exception as e:

            st.error(
                f"Error importing file: {e}"
            )


# ============================================================
# AI HEALTH CHATBOT
# ============================================================

elif menu == "Health Chatbot":

    st.header(
        "🤖 AI Health Chatbot"
    )

    st.write(
        "Ask a general health or wellness question "
        "and get assistance from our AI Health Assistant."
    )

    question = st.text_input(
        "Ask your health question"
    )

    if st.button(
        "Ask AI Assistant"
    ):

        if question.strip():

            try:

                api_key = st.secrets[
                    "GEMINI_API_KEY"
                ]

                answer = health_chatbot(
                    question,
                    api_key
                )

                st.subheader(
                    "🤖 AI Health Assistant"
                )

                st.write(
                    answer
                )

            except Exception as e:

                st.error(
                    f"Unable to connect to AI Health Assistant: {e}"
                )

        else:

            st.warning(
                "Please enter a health question."
            )


# ============================================================
# LOGOUT
# ============================================================

elif menu == "Logout":

    st.session_state.logged_in = False

    st.session_state.page = "Login"

    st.success(
        "Logged out successfully!"
    )

    st.rerun()