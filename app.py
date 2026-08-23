import streamlit as st
import sqlite3

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

from caregiver import (
    add_caregiver,
    view_caregivers
)

from health_chatbot import health_chatbot

from health_api import (
    get_steps,
    get_calories,
    get_water
)

from user import (
    register_user,
    login_user
)

from database import view_fitness

from health_analysis import (
    analyze_fitness_data,
    create_fitness_chart,
    create_calories_chart,
    create_water_chart
)

from health_goals import (
    get_health_goal_progress,
    get_goal_status,
    get_goal_analytics
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

from health_risk import (
    calculate_health_risk
)


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


# ============================================================
# LOGIN / REGISTER
# ============================================================

if not st.session_state.logged_in:

    if st.session_state.page == "Register":

        st.title("🩺 AI Personal Health Assistant")

        st.header("📝 User Registration")

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Register",
            use_container_width=True
        ):

            if username.strip() and password.strip():

                if register_user(username, password):

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


    elif st.session_state.page == "Login":

        st.title("🩺 AI Personal Health Assistant")

        st.header("🔐 User Login")

        username = st.text_input("Username")

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
        "Medication Interaction",
        "Fitness Tracker",
        "Health Goals",
        "Health Risk & Alerts",
        "Health Report",
        "Health Data",
        "Family & Caregiver",
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
    # GET CURRENT DATA
    # --------------------------------------------------------

    steps = get_steps()

    calories = get_calories()

    water = get_water()

    adherence = calculate_adherence()

    fitness_data = view_fitness()

    medicines = view_medicines()

    caregivers = view_caregivers()


    # --------------------------------------------------------
    # TODAY'S HEALTH SUMMARY
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
            "💊 Medication Adherence",
            f"{adherence:.1f}%"
        )

    st.divider()


    # --------------------------------------------------------
    # HEALTH RISK OVERVIEW
    # --------------------------------------------------------

    st.subheader(
        "🚨 Overall Health Risk"
    )

    risk_level, risk_score, warnings = calculate_health_risk(
        steps,
        water,
        calories,
        adherence
    )

    col1, col2 = st.columns(2)

    with col1:

        if "High" in risk_level:

            st.error(
                f"🔴 {risk_level}"
            )

        elif "Moderate" in risk_level:

            st.warning(
                f"🟠 {risk_level}"
            )

        else:

            st.success(
                f"🟢 {risk_level}"
            )

    with col2:

        st.metric(
            "📊 Risk Score",
            risk_score
        )

    if warnings:

        st.subheader(
            "⚠️ Health Warnings"
        )

        for warning in warnings:

            st.warning(
                warning
            )

    else:

        st.success(
            "✅ No major health warnings detected "
            "from the available data."
        )

    # --------------------------------------------------------
    # QUICK RECOMMENDATION
    # --------------------------------------------------------

    st.subheader(
        "💡 Quick Recommendation"
    )

    if "High" in risk_level:

        st.error(
            "🚨 Several health indicators require attention. "
            "Improve your daily health habits and consult "
            "a qualified healthcare professional for "
            "personal medical concerns."
        )

    elif "Moderate" in risk_level:

        st.warning(
            "⚠️ Some health indicators could be improved. "
            "Try to increase physical activity, maintain "
            "adequate hydration, and follow your medication routine."
        )

    else:

        st.success(
            "✅ Your recorded health indicators are currently "
            "within the basic ranges used by this educational system. "
            "Continue maintaining healthy habits."
        )

    st.caption(
        "⚠️ Health risk information is educational only "
        "and is not a medical diagnosis."
    )

    st.divider()


    # --------------------------------------------------------
    # DAILY HEALTH GOALS
    # --------------------------------------------------------

    st.subheader(
        "🎯 Daily Health Goals"
    )

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

    overall_progress = (
        progress["steps"]
        + progress["water"]
        + progress["calories"]
    ) / 3

    st.metric(
        "🌟 Overall Goal Progress",
        f"{overall_progress:.1f}%"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.write(
            "👣 Steps Goal"
        )

        st.progress(
            min(
                int(progress["steps"]),
                100
            ) / 100
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
            min(
                int(progress["water"]),
                100
            ) / 100
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
            min(
                int(progress["calories"]),
                100
            ) / 100
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
    # HEALTH INSIGHTS
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
            f"*{len(medicines)} active medicine(s)* saved."
        )

        for medicine in medicines:

            st.write(
                f"💊 {medicine[1]} | "
                f"Dosage: {medicine[2]} | "
                f"Time: {medicine[3]}"
            )

    else:

        st.info(
            "No active medicines have been saved yet."
        )

    st.divider()


    # --------------------------------------------------------
    # CAREGIVER SUMMARY
    # --------------------------------------------------------

    st.subheader(
        "👨‍👩‍👧 Family & Caregiver"
    )

    if caregivers:

        st.write(
            f"👨‍👩‍👧 {len(caregivers)} caregiver(s) registered."
        )

        if "High" in risk_level:

            st.error(
                "🚨 Caregiver Attention Required"
            )

        elif "Moderate" in risk_level:

            st.warning(
                "⚠️ Caregiver Monitoring Recommended"
            )

        else:

            st.success(
                "🟢 No Immediate Caregiver Action Required"
            )

    else:

        st.info(
            "No caregiver has been added yet."
        )

    st.divider()


    # --------------------------------------------------------
    # HEALTH REPORT
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

    st.subheader(
        "📊 Today's Medication Adherence"
    )

    adherence = calculate_adherence()

    st.progress(
        min(
            int(adherence),
            100
        ) / 100
    )

    st.write(
        f"💊 Adherence: *{adherence:.1f}%*"
    )

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
# MEDICATION INTERACTION
# ============================================================

elif menu == "Medication Interaction":

    st.header(
        "💊 Medication Interaction Checker"
    )

    st.write(
        "Check basic known interactions between two medicines."
    )

    st.warning(
        "⚠️ This tool is for educational purposes only. "
        "It does not replace advice from a doctor or pharmacist."
    )

    st.divider()

    medicine1 = st.text_input(
        "💊 Medicine 1",
        placeholder="Example: Warfarin"
    )

    medicine2 = st.text_input(
        "💊 Medicine 2",
        placeholder="Example: Aspirin"
    )

    if st.button(
        "🔍 Check Interaction",
        use_container_width=True
    ):

        if medicine1.strip() and medicine2.strip():

            try:

                from medication_interaction import (
                    check_medication_interaction
                )

                result = check_medication_interaction(
                    medicine1,
                    medicine2
                )

                st.subheader(
                    "📋 Interaction Result"
                )

                if "Potential Medication Interaction" in result:

                    st.error(result)

                elif "same medicine" in result.lower():

                    st.warning(result)

                else:

                    st.info(result)

            except Exception as e:

                st.error(
                    f"Unable to check interaction: {e}"
                )

        else:

            st.warning(
                "Please enter both medicine names."
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

        analytics = get_goal_analytics(
            steps,
            steps_goal,
            water,
            water_goal,
            calories,
            calories_goal
        )

        st.subheader(
            "📊 Your Goal Progress"
        )

        st.metric(
            "🌟 Overall Wellness Progress",
            f"{analytics['overall']:.1f}%"
        )

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:

            st.write(
                "👣 Steps"
            )

            st.progress(
                min(
                    int(analytics["steps"]["progress"]),
                    100
                ) / 100
            )

            st.write(
                f"Progress: "
                f"{analytics['steps']['progress']:.1f}%"
            )

            st.write(
                f"Current: {analytics['steps']['current']}"
            )

            st.write(
                f"Goal: {analytics['steps']['goal']}"
            )

            st.write(
                f"Remaining: {analytics['steps']['remaining']}"
            )

            st.caption(
                analytics["steps"]["status"]
            )

        with col2:

            st.write(
                "💧 Water"
            )

            st.progress(
                min(
                    int(analytics["water"]["progress"]),
                    100
                ) / 100
            )

            st.write(
                f"Progress: "
                f"{analytics['water']['progress']:.1f}%"
            )

            st.write(
                f"Current: {analytics['water']['current']} L"
            )

            st.write(
                f"Goal: {analytics['water']['goal']} L"
            )

            st.write(
                f"Remaining: {analytics['water']['remaining']} L"
            )

            st.caption(
                analytics["water"]["status"]
            )

        with col3:

            st.write(
                "🔥 Calories"
            )

            st.progress(
                min(
                    int(analytics["calories"]["progress"]),
                    100
                ) / 100
            )

            st.write(
                f"Progress: "
                f"{analytics['calories']['progress']:.1f}%"
            )

            st.write(
                f"Current: {analytics['calories']['current']}"
            )

            st.write(
                f"Goal: {analytics['calories']['goal']}"
            )

            st.write(
                f"Remaining: {analytics['calories']['remaining']}"
            )

            st.caption(
                analytics["calories"]["status"]
            )


# ============================================================
# HEALTH RISK & ALERTS
# ============================================================

elif menu == "Health Risk & Alerts":

    st.header(
        "🚨 Health Risk & Alerts"
    )

    st.write(
        "Automatically analyze your current fitness "
        "and medication data to identify basic health risks."
    )

    st.warning(
        "⚠️ This assessment is for educational purposes only "
        "and is not a medical diagnosis."
    )

    st.divider()

    steps = get_steps()

    water = get_water()

    calories = get_calories()

    adherence = calculate_adherence()

    st.subheader(
        "📊 Current Health Status"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "👣 Steps",
            steps
        )

    with col2:

        st.metric(
            "💧 Water",
            f"{water} L"
        )

    with col3:

        st.metric(
            "🔥 Calories",
            calories
        )

    with col4:

        st.metric(
            "💊 Medication Adherence",
            f"{adherence:.1f}%"
        )

    st.divider()

    risk_level, risk_score, warnings = calculate_health_risk(
        steps,
        water,
        calories,
        adherence
    )

    st.subheader(
        "🚨 Overall Health Risk"
    )

    if "High" in risk_level:

        st.error(
            f"{risk_level} | Risk Score: {risk_score}"
        )

    elif "Moderate" in risk_level:

        st.warning(
            f"{risk_level} | Risk Score: {risk_score}"
        )

    else:

        st.success(
            f"{risk_level} | Risk Score: {risk_score}"
        )

    st.divider()

    st.subheader(
        "⚠️ Health Alerts"
    )

    if warnings:

        for warning in warnings:

            st.warning(
                warning
            )

    else:

        st.success(
            "✅ No major health warnings detected "
            "from the available data."
        )

    st.divider()

    st.subheader(
        "💡 Recommendation"
    )

    if "High" in risk_level:

        st.error(
            "Several health indicators require attention. "
            "Consider improving your daily health habits "
            "and consult a qualified healthcare professional "
            "for personal medical concerns."
        )

    elif "Moderate" in risk_level:

        st.warning(
            "Some health indicators could be improved. "
            "Try to increase physical activity, maintain "
            "adequate hydration, and follow your medication routine."
        )

    else:

        st.success(
            "Your recorded health indicators are currently "
            "within the basic ranges used by this educational system. "
            "Continue maintaining healthy habits."
        )

    st.caption(
        "⚠️ This risk assessment is for educational purposes only "
        "and is not a medical diagnosis."
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
        "Add a trusted caregiver and monitor important health information."
    )

    st.warning(
        "⚠️ Caregiver alerts are based on the health indicators "
        "available in this educational system."
    )

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

    st.subheader(
        "📊 Current Health Status"
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

    st.subheader(
        "🚨 Caregiver Health Alert"
    )

    risk_level, risk_score, warnings = calculate_health_risk(
        steps,
        water,
        calories,
        adherence
    )

    if "High" in risk_level:

        st.error(
            f"🚨 HIGH HEALTH RISK | Risk Score: {risk_score}"
        )

        st.error(
            "Caregiver attention is recommended."
        )

    elif "Moderate" in risk_level:

        st.warning(
            f"⚠️ MODERATE HEALTH RISK | Risk Score: {risk_score}"
        )

        st.warning(
            "Caregiver should monitor the user's health indicators."
        )

    else:

        st.success(
            f"🟢 LOW HEALTH RISK | Risk Score: {risk_score}"
        )

        st.success(
            "No immediate caregiver attention is indicated "
            "by the available health data."
        )

    if warnings:

        st.subheader(
            "⚠️ Reasons for Caregiver Alert"
        )

        for warning in warnings:

            st.warning(
                warning
            )

    else:

        st.info(
            "No specific health warnings were generated."
        )

    st.divider()

    st.subheader(
        "💊 Medication Monitoring"
    )

    if adherence >= 80:

        st.success(
            "✅ Medication adherence is good. "
            "No caregiver attention is currently required."
        )

    elif adherence > 0:

        st.warning(
            "⚠️ Medication adherence is below 80%. "
            "The caregiver should check the medication routine."
        )

    else:

        st.info(
            "ℹ️ No medication adherence records are available yet."
        )

    st.divider()

    st.subheader(
        "📋 Caregiver Summary"
    )

    if caregivers:

        st.write(
            f"👨‍👩‍👧 Registered Caregivers: "
            f"**{len(caregivers)}**"
        )

        if "High" in risk_level:

            st.error(
                "🚨 Caregiver notification status: "
                "**ATTENTION REQUIRED**"
            )

        elif "Moderate" in risk_level:

            st.warning(
                "⚠️ Caregiver notification status: "
                "**MONITOR REQUIRED**"
            )

        else:

            st.success(
                "🟢 Caregiver notification status: "
                "**NO IMMEDIATE ACTION REQUIRED**"
            )

    else:

        st.warning(
            "No caregiver is registered. "
            "Consider adding a trusted caregiver."
        )

    st.caption(
        "⚠️ These alerts are educational and do not replace "
        "professional medical advice."
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
        "🤖 Ask AI Assistant",
        use_container_width=True
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