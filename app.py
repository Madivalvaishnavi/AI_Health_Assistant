import streamlit as st
import sqlite3

# ============================================================
# HOME PAGE
# ============================================================

from home import home_page


# ============================================================
# MEDICATION
# ============================================================

from medicine import (
    add_medicine,
    view_medicines,
    mark_medication_status,
    view_today_adherence,
    calculate_adherence,
    delete_medicine,
    complete_medicine,
    view_medication_history
)


# ============================================================
# CAREGIVER
# ============================================================

from caregiver import (
    add_caregiver,
    view_caregivers
)


# ============================================================
# HEALTH API
# ============================================================

from health_api import (
    get_steps,
    get_calories,
    get_water
)


# ============================================================
# USER AUTHENTICATION
# ============================================================

from user import (
    register_user,
    login_user
)


# ============================================================
# DATABASE
# ============================================================

from database import (
    view_fitness
)


# ============================================================
# HEALTH ANALYSIS
# ============================================================

from health_analysis import (
    analyze_fitness_data,
    create_fitness_chart,
    create_calories_chart,
    create_water_chart
)


# ============================================================
# HEALTH GOALS
# ============================================================

from health_goals import (
    get_health_goal_progress,
    get_goal_status,
    get_goal_analytics
)


# ============================================================
# HEALTH REPORT
# ============================================================

from health_report import (
    generate_health_report
)


# ============================================================
# HEALTH DATA FORMATS
# ============================================================

from health_data_formats import (
    export_json,
    export_csv,
    export_xml,
    import_json,
    import_csv,
    import_xml
)


# ============================================================
# AI HEALTH CHATBOT
# ============================================================

from health_chatbot import health_chatbot


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🩺",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Register"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_your_health" not in st.session_state:
    st.session_state.show_your_health = False


# ============================================================
# LOGIN / REGISTER
# ============================================================

if not st.session_state.logged_in:

    # ========================================================
    # REGISTER
    # ========================================================

    if st.session_state.page == "Register":

        st.title("🩺 AI Personal Health Assistant")

        st.header("📝 User Registration")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Register",
            use_container_width=True
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
            "Go to Login",
            use_container_width=True
        ):

            st.session_state.page = "Login"

            st.rerun()


    # ========================================================
    # LOGIN
    # ========================================================

    elif st.session_state.page == "Login":

        st.title(
            "🩺 AI Personal Health Assistant"
        )

        st.header(
            "🔐 User Login"
        )

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            user = login_user(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True

                st.session_state.show_your_health = False

                st.success(
                    "Login Successful!"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

        if st.button(
            "Go to Register",
            use_container_width=True
        ):

            st.session_state.page = "Register"

            st.rerun()


    st.stop()


# ============================================================
# APPLICATION TITLE
# ============================================================

st.title(
    "🩺 AI Personal Health Assistant"
)

st.write(
    "Welcome to your AI-powered personal health monitoring assistant!"
)


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
        "Family & Caregiver",
        "Health Chatbot",
        "Logout"
    ]
)


# ============================================================
# HOME
# ============================================================

if menu == "Home":

    home_page()


# ============================================================
# MEDICATION TRACKER
# ============================================================

elif menu == "Medication Tracker":

    st.header(
        "💊 Medication Tracker"
    )

    # --------------------------------------------------------
    # ADD MEDICATION
    # --------------------------------------------------------

    st.subheader(
        "➕ Add Medication"
    )

    medicine_name = st.text_input(
        "Medicine Name"
    )

    dosage = st.text_input(
        "Dosage"
    )

    medicine_time = st.text_input(
        "Time"
    )

    if st.button(
        "💾 Save Medicine",
        use_container_width=True
    ):

        if (
            medicine_name.strip()
            and dosage.strip()
            and medicine_time.strip()
        ):

            add_medicine(
                medicine_name,
                dosage,
                medicine_time
            )

            st.success(
                "Medicine Saved Successfully!"
            )

            st.rerun()

        else:

            st.warning(
                "Please enter medicine name, dosage, and time."
            )

    st.divider()

    # --------------------------------------------------------
    # SAVED MEDICINES
    # --------------------------------------------------------

    st.subheader(
        "📋 Saved Medicines"
    )

    medicines = view_medicines()

    if medicines:

        for medicine in medicines:

            medicine_id = medicine[0]
            medicine_name = medicine[1]
            dosage = medicine[2]
            medicine_time = medicine[3]

            col1, col2, col3 = st.columns(
                [5, 1, 1]
            )

            with col1:

                st.write(
                    f"💊 *{medicine_name}* | "
                    f"Dosage: {dosage} | "
                    f"⏰ {medicine_time}"
                )

            with col2:

                if st.button(
                    "✅ Complete",
                    key=f"complete_{medicine_id}"
                ):

                    complete_medicine(
                        medicine_id
                    )

                    st.success(
                        f"{medicine_name} marked as completed."
                    )

                    st.rerun()

            with col3:

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{medicine_id}"
                ):

                    delete_medicine(
                        medicine_id
                    )

                    st.success(
                        f"{medicine_name} deleted successfully."
                    )

                    st.rerun()

    else:

        st.info(
            "No active medicines saved yet."
        )

    st.divider()

    # --------------------------------------------------------
    # MEDICATION ADHERENCE
    # --------------------------------------------------------

    st.subheader(
        "💊 Medication Adherence Monitoring"
    )

    st.write(
        "Mark your medication as Taken or Missed."
    )

    if medicines:

        for medicine in medicines:

            medicine_id = medicine[0]
            medicine_name = medicine[1]
            dosage = medicine[2]
            medicine_time = medicine[3]

            st.write(
                f"💊 *{medicine_name}* | "
                f"{dosage} | "
                f"⏰ {medicine_time}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✅ Taken",
                    key=f"taken_{medicine_id}"
                ):

                    mark_medication_status(
                        medicine_id,
                        "Taken"
                    )

                    st.success(
                        f"{medicine_name} marked as Taken."
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "❌ Missed",
                    key=f"missed_{medicine_id}"
                ):

                    mark_medication_status(
                        medicine_id,
                        "Missed"
                    )

                    st.warning(
                        f"{medicine_name} marked as Missed."
                    )

                    st.rerun()

    else:

        st.info(
            "Add a medicine first to track adherence."
        )

    st.divider()

    # --------------------------------------------------------
    # TODAY'S ADHERENCE
    # --------------------------------------------------------

    st.subheader(
        "📊 Today's Medication Adherence"
    )

    adherence = calculate_adherence()

    st.progress(
        min(int(adherence), 100) / 100
    )

    st.write(
        f"💊 Adherence: *{adherence:.1f}%*"
    )

    # --------------------------------------------------------
    # TODAY'S MEDICATION STATUS
    # --------------------------------------------------------

    adherence_records = view_today_adherence()

    if adherence_records:

        st.subheader(
            "📋 Today's Medication Status"
        )

        for record in adherence_records:

            medicine_name = record[1]
            dosage = record[2]
            medicine_time = record[3]
            status = record[4]

            if status == "Taken":

                st.success(
                    f"💊 {medicine_name} | "
                    f"{dosage} | "
                    f"{medicine_time} | "
                    f"✅ {status}"
                )

            elif status == "Missed":

                st.error(
                    f"💊 {medicine_name} | "
                    f"{dosage} | "
                    f"{medicine_time} | "
                    f"❌ {status}"
                )

            else:

                st.warning(
                    f"💊 {medicine_name} | "
                    f"{dosage} | "
                    f"{medicine_time} | "
                    f"⏳ {status}"
                )

    # --------------------------------------------------------
    # MEDICATION HISTORY
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "📜 Medication Adherence History"
    )

    history = view_medication_history()

    if history:

        history_data = []

        for record in history:

            history_data.append(
                {
                    "Date": record[4],
                    "Medicine": record[1],
                    "Dosage": record[2],
                    "Time": record[3],
                    "Status": (
                        "✅ Taken"
                        if record[5] == "Taken"
                        else "❌ Missed"
                    )
                }
            )

        st.dataframe(
            history_data,
            use_container_width=True,
            hide_index=True
        )

        st.subheader(
            "📊 Overall Medication Adherence"
        )

        total_records = len(history)

        taken_records = sum(
            1
            for record in history
            if record[5] == "Taken"
        )

        missed_records = sum(
            1
            for record in history
            if record[5] == "Missed"
        )

        if total_records > 0:

            overall_adherence = (
                taken_records / total_records
            ) * 100

        else:

            overall_adherence = 0

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Total Records",
                total_records
            )

        with col2:

            st.metric(
                "✅ Taken",
                taken_records
            )

        with col3:

            st.metric(
                "❌ Missed",
                missed_records
            )

        with col4:

            st.metric(
                "📊 Adherence",
                f"{overall_adherence:.1f}%"
            )

    else:

        st.info(
            "No medication history available yet."
        )


# ============================================================
# FITNESS TRACKER
# ============================================================

elif menu == "Fitness Tracker":

    st.header(
        "🏃 Fitness Tracker"
    )

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

    if st.button(
        "💾 Save Fitness Data",
        use_container_width=True
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

            st.info(insight)

        st.divider()

        st.subheader(
            "📊 Health Data Visualization"
        )

        st.write(
            "👣 Steps Progress"
        )

        steps_chart = create_fitness_chart(
            fitness_data
        )

        if steps_chart:

            st.pyplot(
                steps_chart,
                use_container_width=True
            )

        st.write(
            "🔥 Calories Burned Progress"
        )

        calories_chart = create_calories_chart(
            fitness_data
        )

        if calories_chart:

            st.pyplot(
                calories_chart,
                use_container_width=True
            )

        st.write(
            "💧 Water Intake Progress"
        )

        water_chart = create_water_chart(
            fitness_data
        )

        if water_chart:

            st.pyplot(
                water_chart,
                use_container_width=True
            )

        st.subheader(
            "📋 Saved Fitness Records"
        )

        for record in fitness_data:

            st.write(record)

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
        "📊 Calculate Goal Progress",
        use_container_width=True
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

            st.write("👣 Steps")

            st.progress(
                min(int(progress["steps"]), 100) / 100
            )

            st.write(
                f"{progress['steps']:.1f}%"
            )

        with col2:

            st.write("💧 Water")

            st.progress(
                min(int(progress["water"]), 100) / 100
            )

            st.write(
                f"{progress['water']:.1f}%"
            )

        with col3:

            st.write("🔥 Calories")

            st.progress(
                min(int(progress["calories"]), 100) / 100
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
# HEALTH DATA
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

            if file_name.endswith(".json"):

                imported_data = import_json(
                    uploaded_file
                )

            elif file_name.endswith(".csv"):

                imported_data = import_csv(
                    uploaded_file
                )

            elif file_name.endswith(".xml"):

                imported_data = import_xml(
                    uploaded_file
                )

            else:

                imported_data = None

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
# FAMILY & CAREGIVER
# ============================================================

elif menu == "Family & Caregiver":

    st.header(
        "👨‍👩‍👧 Family & Caregiver Monitoring"
    )

    st.write(
        "Add a trusted caregiver to monitor important health information."
    )

    # --------------------------------------------------------
    # ADD CAREGIVER
    # --------------------------------------------------------

    st.subheader(
        "➕ Add Caregiver"
    )

    caregiver_name = st.text_input(
        "Caregiver Name"
    )

    caregiver_contact = st.text_input(
        "Caregiver Contact"
    )

    if st.button(
        "💾 Save Caregiver",
        use_container_width=True
    ):

        if (
            caregiver_name.strip()
            and caregiver_contact.strip()
        ):

            add_caregiver(
                caregiver_name,
                caregiver_contact
            )

            st.success(
                "Caregiver added successfully!"
            )

            st.rerun()

        else:

            st.warning(
                "Please enter caregiver name and contact."
            )

    st.divider()

    # --------------------------------------------------------
    # SAVED CAREGIVERS
    # --------------------------------------------------------

    st.subheader(
        "📋 Saved Caregivers"
    )

    caregivers = view_caregivers()

    if caregivers:

        for caregiver in caregivers:

            st.write(
                f"👤 *{caregiver[1]}* | "
                f"📞 {caregiver[2]}"
            )

    else:

        st.info(
            "No caregivers added yet."
        )

    st.divider()

    # --------------------------------------------------------
    # HEALTH STATUS
    # --------------------------------------------------------

    st.subheader(
        "📊 Health Status"
    )

    steps = get_steps()

    calories = get_calories()

    water = get_water()

    adherence = calculate_adherence()

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
            "💊 Medication Adherence",
            f"{adherence:.1f}%"
        )

    st.divider()

    # --------------------------------------------------------
    # CAREGIVER NOTIFICATION
    # --------------------------------------------------------

    st.subheader(
        "🔔 Caregiver Notification"
    )

    if adherence >= 80:

        st.success(
            "✅ Medication adherence is good. "
            "No caregiver attention is currently required."
        )

    elif adherence > 0:

        st.warning(
            "⚠️ Medication adherence is below 80%. "
            "The caregiver should be informed to check medication routines."
        )

    else:

        st.info(
            "ℹ️ No medication adherence records are available yet."
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

    st.info(
        "💡 You can ask about symptoms, medicines, nutrition, "
        "fitness, diseases, healthy habits, and general health."
    )

    question = st.text_input(
        "Ask your health question",
        placeholder="Example: What should I do if I have a headache?"
    )

    if st.button(
        "🤖 Ask AI Assistant",
        use_container_width=True
    ):

        if question.strip():

            try:

                # ------------------------------------------------
                # GET GEMINI API KEY FROM STREAMLIT SECRETS
                # ------------------------------------------------

                api_key = st.secrets["GEMINI_API_KEY"]

                # ------------------------------------------------
                # CALL AI HEALTH CHATBOT
                # ------------------------------------------------

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

            except KeyError:

                st.error(
                    "❌ GEMINI_API_KEY is not configured. "
                    "Please add it to .streamlit/secrets.toml."
                )

            except Exception as e:

                st.error(
                    f"❌ Unable to connect to AI Health Assistant: {e}"
                )

        else:

            st.warning(
                "⚠️ Please enter a health question."
            )


# ============================================================
# LOGOUT
# ============================================================

elif menu == "Logout":

    st.session_state.logged_in = False

    st.session_state.page = "Login"

    st.session_state.show_your_health = False

    st.success(
        "Logged out successfully!"
    )

    st.rerun()