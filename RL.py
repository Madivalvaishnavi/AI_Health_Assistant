import streamlit as st
import re

from user import register_user, login_user, reset_password


# ============================================================
# PASSWORD VALIDATION
# ============================================================

def validate_password(password):

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one alphabet."

    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."

    if not re.search(r"[^A-Za-z0-9]", password):
        return False, "Password must contain at least one special character."

    return True, ""


# ============================================================
# REGISTRATION PAGE
# ============================================================

def registration_page():

    st.title("🩺 AI Personal Health Assistant")
    st.header("📝 User Registration")

    username = st.text_input(
        "👤 Username",
        key="reg_username"
    )

    password = st.text_input(
        "🔐 Password",
        type="password",
        key="reg_password"
    )

    confirm_password = st.text_input(
        "🔐 Confirm Password",
        type="password",
        key="reg_confirm_password"
    )

    st.caption(
        "Password: minimum 8 characters + alphabet + number + special character"
    )

    if st.button(
        "📝 Register",
        use_container_width=True
    ):

        if not username.strip():

            st.warning("Please enter username.")

        elif not password:

            st.warning("Please enter password.")

        elif password != confirm_password:

            st.error("❌ Passwords do not match.")

        else:

            valid, message = validate_password(password)

            if not valid:

                st.error(f"❌ {message}")

            else:

                result = register_user(
                    username.strip(),
                    password
                )

                if result:

                    st.session_state.page = "Registration Success"

                    st.rerun()

                else:

                    st.error(
                        "❌ Username already exists!"
                    )

    st.divider()

    if st.button(
        "🔐 Already have an account? Login",
        use_container_width=True
    ):

        st.session_state.page = "Login"

        st.rerun()


# ============================================================
# REGISTRATION SUCCESS
# ============================================================

def registration_success_page():

    st.title("🎉 Registration Successful!")

    st.success(
        "Your account has been created successfully."
    )

    st.write(
        "Welcome to AI Personal Health Assistant! 🩺"
    )

    st.write(
        "Your health journey starts here. 💙"
    )

    if st.button(
        "🔐 Continue to Login",
        use_container_width=True
    ):

        st.session_state.page = "Login"

        st.rerun()


# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():

    st.title("🩺 AI Personal Health Assistant")
    st.header("🔐 User Login")

    username = st.text_input(
        "👤 Username",
        key="login_username"
    )

    password = st.text_input(
        "🔐 Password",
        type="password",
        key="login_password"
    )

    if st.button(
        "🔐 Login",
        use_container_width=True
    ):

        if not username.strip():

            st.warning("Please enter username.")

        elif not password:

            st.warning("Please enter password.")

        else:

            user = login_user(
                username.strip(),
                password
            )

            if user:

                st.session_state.logged_in = True

                st.session_state.current_user = username.strip()

                st.session_state.page = "Login Success"

                st.rerun()

            else:

                st.error(
                    "❌ Invalid Username or Password."
                )

    st.divider()

    # FORGOT PASSWORD

    if st.button(
        "🔑 Forgot Password?",
        use_container_width=True
    ):

        st.session_state.page = "Forgot Password"

        st.rerun()

    if st.button(
        "📝 Create a New Account",
        use_container_width=True
    ):

        st.session_state.page = "Register"

        st.rerun()


# ============================================================
# FORGOT PASSWORD
# ============================================================

def forgot_password_page():

    st.title("🔑 Forgot Password")

    st.header("Reset Your Password")

    username = st.text_input(
        "👤 Username",
        key="forgot_username"
    )

    new_password = st.text_input(
        "🔐 New Password",
        type="password",
        key="new_password"
    )

    confirm_password = st.text_input(
        "🔐 Confirm New Password",
        type="password",
        key="confirm_new_password"
    )

    st.caption(
        "Password: minimum 8 characters + alphabet + number + special character"
    )

    if st.button(
        "🔄 Reset Password",
        use_container_width=True
    ):

        if not username.strip():

            st.warning("Please enter username.")

        elif not new_password:

            st.warning("Please enter new password.")

        elif new_password != confirm_password:

            st.error("❌ Passwords do not match.")

        else:

            valid, message = validate_password(
                new_password
            )

            if not valid:

                st.error(f"❌ {message}")

            else:

                result = reset_password(
                    username.strip(),
                    new_password
                )

                if result:

                    st.success(
                        "✅ Password reset successfully!"
                    )

                    st.session_state.page = "Login"

                    st.rerun()

                else:

                    st.error(
                        "❌ Username not found."
                    )

    st.divider()

    if st.button(
        "⬅️ Back to Login",
        use_container_width=True
    ):

        st.session_state.page = "Login"

        st.rerun()


# ============================================================
# LOGIN SUCCESS
# ============================================================

def login_success_page():

    username = st.session_state.get(
        "current_user",
        "User"
    )

    st.title("🎉 Login Successful!")

    st.success(
        f"Welcome back, {username}! 👋"
    )

    st.write(
        "Your AI Personal Health Assistant is ready. 🩺"
    )

    if st.button(
        "🏠 Enter Health Assistant",
        use_container_width=True
    ):

        st.session_state.page = "Home"

        st.rerun()


# ============================================================
# LOGOUT SUCCESS
# ============================================================

def logout_success_page():

    st.title("👋 Logged Out Successfully!")

    st.success(
        "You have been safely logged out."
    )

    st.write(
        "Thank you for using AI Personal Health Assistant. 💙"
    )

    if st.button(
        "🔐 Login Again",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.session_state.current_user = None

        st.session_state.page = "Login"

        st.rerun()