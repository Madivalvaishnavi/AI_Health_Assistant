import streamlit as st
import sqlite3

from medicine import add_medicine, view_medicines
from health_chatbot import health_chatbot
from health_api import get_steps, get_calories, get_water
from user import register_user, login_user

from database import view_fitness

from health_analysis import (
    analyze_fitness_data,
    create_fitness_chart
)

from health_goals import (
    get_health_goal_progress,
    get_goal_status
)

from health_report import (
    generate_health_report
)

from health_data_formats import (
    export_json,
    export_csv,
    export_xml,
    import_json,
    import_csv,
    import_xml
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 AI Personal Health Assistant")
st.write(
    "Welcome to your AI-powered personal health monitoring assistant!"
)


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

    # --------------------------------------------------------
    # REGISTER
    # --------------------------------------------------------

    if st.session_state.page == "Register":

        st.header("📝 User Registration")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Register"
        ):

            if username.strip() and password.strip():

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


        if st.button(
            "Go to Login"
        ):

            st.session_state.page = "Login"

            st.rerun()


    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    elif st.session_state.page == "Login":

        st.header("🔐 User Login")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Login"
        ):

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


        if st.button(
            "Go to Register"
        ):

            st.session_state.page = "Register"

            st.rerun()


    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

menu = st.sidebar.selectbox(
    "🩺 Choose Option",
    [
        "Home",
        "Medication Tracker",
        "Fitness Tracker",
        "Health Goals",
        "Health Report",
        "Health Data",
        "Health Chatbot",
        "Logout"
    ]
)


# ============================================================
# HOME DASHBOARD
# ============================================================

if menu == "Home":

    st.header(
        "🏠 Health Monitoring Dashboard"
    )

    st.write(
        "Your complete health overview in one place."
    )


    # --------------------------------------------------------
    # GET CURRENT FITNESS DATA
    # --------------------------------------------------------

    steps = get_steps()

    calories = get_calories()

    water = get_water()


    # --------------------------------------------------------
    # GET SAVED DATA
    # --------------------------------------------------------

    fitness_data = view_fitness()

    medicines = view_medicines()


    # --------------------------------------------------------
    # FITNESS SUMMARY
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # HEALTH GOALS
    # --------------------------------------------------------

    st.subheader(
        "🎯 Daily Health Goals"
    )


    # Default goals

    steps_goal = 10000

    water_goal = 3

    calories_goal = 500


    progress = get_health_goal_progress(
        steps,
        steps_goal,
        water,
        water_goal,
        calories,
        calories_goal
    )


    # --------------------------------------------------------
    # GOAL PROGRESS COLUMNS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        st.write(
            "👣 Steps Goal"
        )

        st.progress(
            int(progress["steps"]) / 100
        )

        st.write(
            f"{progress['steps']:.1f}% completed"
        )

        st.caption(
            get_goal_status(
                steps,
                steps_goal
            )
        )


    with col2:

        st.write(
            "💧 Water Goal"
        )

        st.progress(
            int(progress["water"]) / 100
        )

        st.write(
            f"{progress['water']:.1f}% completed"
        )

        st.caption(
            get_goal_status(
                water,
                water_goal
            )
        )


    with col3:

        st.write(
            "🔥 Calories Goal"
        )

        st.progress(
            int(progress["calories"]) / 100
        )

        st.write(
            f"{progress['calories']:.1f}% completed"
        )

        st.caption(
            get_goal_status(
                calories,
                calories_goal
            )
        )


    st.divider()


    # --------------------------------------------------------
    # HEALTH ANALYSIS
    # --------------------------------------------------------

    st.subheader(
        "💡 Health Insights"
    )


    if fitness_data:

        analysis, insights = analyze_fitness_data(
            fitness_data
        )

        for insight in insights:

            st.info(
                insight
            )

    else:

        st.info(
            "Add fitness data to receive health insights."
        )


    st.divider()


    # --------------------------------------------------------
    # MEDICATION SUMMARY
    # --------------------------------------------------------

    st.subheader(
        "💊 Medication Summary"
    )


    if medicines:

        st.write(
            f"You currently have "
            f"**{len(medicines)} medicine(s)** saved."
        )

        for medicine in medicines:

            st.write(
                f"💊 {medicine[1]} | "
                f"Dosage: {medicine[2]} | "
                f"Time: {medicine[3]}"
            )

    else:

        st.info(
            "No medicines have been saved yet."
        )


    st.divider()


    # --------------------------------------------------------
    # QUICK HEALTH REPORT
    # --------------------------------------------------------

    st.subheader(
        "📄 Health Report"
    )


    if fitness_data:

        report = generate_health_report(
            fitness_data,
            medicines
        )

        st.download_button(
            label="📥 Download Health Report",
            data=report,
            file_name="health_report.txt",
            mime="text/plain"
        )

    else:

        st.info(
            "Add fitness data to generate your health report."
        )


# ============================================================
# MEDICATION TRACKER
# ============================================================

elif menu == "Medication Tracker":

    st.header(
        "💊 Medication Tracker"
    )


    medicine_name = st.text_input(
        "Medicine Name"
    )

    dosage = st.text_input(
        "Dosage"
    )

    time = st.text_input(
        "Time"
    )


    if st.button(
        "Save Medicine"
    ):

        if (
            medicine_name.strip()
            and dosage.strip()
            and time.strip()
        ):

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
                f"💊 {medicine[1]} | "
                f"Dosage: {medicine[2]} | "
                f"Time: {medicine[3]}"
            )

    else:

        st.info(
            "No medicines saved yet."
        )


# ============================================================
# FITNESS TRACKER
# ============================================================

elif menu == "Fitness Tracker":

    st.header(
        "🏃 Fitness Tracker"
    )


    # --------------------------------------------------------
    # ENTER FITNESS DATA
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # SAVE FITNESS DATA
    # --------------------------------------------------------

    if st.button(
        "Save Fitness Data"
    ):

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


    st.divider()


    # --------------------------------------------------------
    # CURRENT FITNESS DATA
    # --------------------------------------------------------

    st.subheader(
        "📊 Current Fitness Data"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "👣 Steps",
            get_steps()
        )


    with col2:

        st.metric(
            "🔥 Calories",
            get_calories()
        )


    with col3:

        st.metric(
            "💧 Water",
            f"{get_water()} L"
        )


    st.divider()


    # --------------------------------------------------------
    # FITNESS ANALYSIS
    # --------------------------------------------------------

    fitness_data = view_fitness()


    st.subheader(
        "📈 Health Data Analysis"
    )


    if fitness_data:

        analysis, insights = analyze_fitness_data(
            fitness_data
        )


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


        st.subheader(
            "💡 Health Insights"
        )


        for insight in insights:

            st.info(
                insight
            )


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


        st.subheader(
            "📋 Saved Fitness Records"
        )


        for record in fitness_data:

            st.write(
                record
            )


    else:

        st.info(
            "No fitness records found yet."
        )


# ============================================================
# HEALTH GOALS
# ============================================================

elif menu == "Health Goals":

    st.header(
        "🎯 Health Goals"
    )


    st.write(
        "Track your progress toward your daily health goals."
    )


    # Default goals

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


    steps = get_steps()

    water = get_water()

    calories = get_calories()


    if st.button(
        "Calculate Goal Progress"
    ):

        progress = get_health_goal_progress(
            steps,
            steps_goal,
            water,
            water_goal,
            calories,
            calories_goal
        )


        st.subheader(
            "📊 Your Progress"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.write(
                "👣 Steps"
            )

            st.progress(
                int(progress["steps"]) / 100
            )

            st.write(
                f"{progress['steps']:.1f}%"
            )


        with col2:

            st.write(
                "💧 Water"
            )

            st.progress(
                int(progress["water"]) / 100
            )

            st.write(
                f"{progress['water']:.1f}%"
            )


        with col3:

            st.write(
                "🔥 Calories"
            )

            st.progress(
                int(progress["calories"]) / 100
            )

            st.write(
                f"{progress['calories']:.1f}%"
            )


# ============================================================
# HEALTH REPORT
# ============================================================

elif menu == "Health Report":

    st.header(
        "📄 Health Report"
    )


    fitness_data = view_fitness()

    medicines = view_medicines()


    if fitness_data:

        report = generate_health_report(
            fitness_data,
            medicines
        )


        st.text_area(
            "Generated Health Report",
            report,
            height=500
        )


        st.download_button(
            label="📥 Download Health Report",
            data=report,
            file_name="health_report.txt",
            mime="text/plain"
        )


    else:

        st.info(
            "No fitness data available. "
            "Please add fitness data first."
        )


# ============================================================
# HEALTH DATA IMPORT / EXPORT
# ============================================================

elif menu == "Health Data":

    st.header(
        "📂 Health Data Management"
    )


    fitness_data = view_fitness()


    # --------------------------------------------------------
    # EXPORT
    # --------------------------------------------------------

    st.subheader(
        "📤 Export Health Data"
    )


    if fitness_data:

        col1, col2, col3 = st.columns(3)


        with col1:

            json_data = export_json(
                fitness_data
            )

            st.download_button(
                "Download JSON",
                json_data,
                "health_data.json",
                "application/json"
            )


        with col2:

            csv_data = export_csv(
                fitness_data
            )

            st.download_button(
                "Download CSV",
                csv_data,
                "health_data.csv",
                "text/csv"
            )


        with col3:

            xml_data = export_xml(
                fitness_data
            )

            st.download_button(
                "Download XML",
                xml_data,
                "health_data.xml",
                "application/xml"
            )


    else:

        st.info(
            "No health data available for export."
        )


    st.divider()


    # --------------------------------------------------------
    # IMPORT
    # --------------------------------------------------------

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


            st.success(
                "Health data imported successfully!"
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