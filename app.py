import streamlit as st
from medicine import add_medicine, view_medicines
from health_chatbot import health_chatbot
from health_api import get_steps, get_calories, get_water
from user import register_user, login_user

st.set_page_config(page_title="AI Health Assistant", page_icon="🩺")

st.title("🩺 AI Personal Health Assistant")
st.write("Welcome to your AI Health Assistant!")

# ---------------- SESSION ----------------

if "page" not in st.session_state:
    st.session_state.page = "Register"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN / REGISTER ----------------

if not st.session_state.logged_in:

    if st.session_state.page == "Register":

        st.header("User Registration")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            if register_user(username, password):
                st.success("Registration Successful! Please Login.")
                st.session_state.page = "Login"
                st.rerun()
            else:
                st.error("Username already exists!")

    elif st.session_state.page == "Login":

        st.header("User Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(username, password)

            if user:
                st.session_state.logged_in = True
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    st.stop()

# ---------------- SIDEBAR ----------------

menu = st.sidebar.selectbox(
    "Choose Option",
    [
        "Home",
        "Medication Tracker",
        "Fitness Tracker",
        "Health Chatbot",
        "Logout"
    ]
)

# ---------------- HOME ----------------

if menu == "Home":

    st.header("🏠 Dashboard")
    st.write("Welcome to AI Personal Health Assistant!")

# ---------------- MEDICATION TRACKER ----------------

elif menu == "Medication Tracker":

    st.header("💊 Medication Tracker")

    medicine_name = st.text_input("Medicine Name")

    dosage = st.text_input("Dosage")

    time = st.text_input("Time")

    if st.button("Save Medicine"):

        add_medicine(medicine_name, dosage, time)

        st.success("Medicine Saved Successfully!")

    st.subheader("Saved Medicines")

    medicines = view_medicines()

    for medicine in medicines:
        st.write(medicine)

# ---------------- FITNESS TRACKER ----------------

elif menu == "Fitness Tracker":

    st.header("🏃 Fitness Tracker")

    st.write("👣 Steps:", get_steps())

    st.write("🔥 Calories:", get_calories())

    st.write("💧 Water Intake:", get_water(), "L")

# ---------------- HEALTH CHATBOT ----------------

elif menu == "Health Chatbot":

    st.header("🤖")