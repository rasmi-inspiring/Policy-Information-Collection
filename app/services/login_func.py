import streamlit as st
import os
from sqlalchemy.orm import Session
from database import (
    SessionLocal,
)
from models import User


# Function to get the user from the database
def get_user_by_username(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()


# Function to handle the login logic
def login():

    try:
        # Check if the user is already logged in
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False

        with st.sidebar:
            image_path = os.path.join("app", "images", "ilab.png")

            # Check if the image exists
            if os.path.exists(image_path):
                # Create a centered column
                col = st.columns([2, 6, 0.4])
                with col[1]:
                    st.image(
                        image_path, use_container_width=False, width=170
                    )  # Adjust width as needed
            else:
                st.warning("Image not found!")

            # # Show login form if not logged in
            if not st.session_state.logged_in:

                st.markdown(
                    """
                            <style>
                                .custom-header {
                                    text-align: center;
                                    font-size: 32px;
                                    font-weight: bold;
                                    margin-top: 10px;
                                    margin-bottom: 10px;
                                }
                            </style>
                            <div class="custom-header">Login</div>
                        """,
                    unsafe_allow_html=True,
                )
                username = st.text_input("Username", key="username_input")
                password = st.text_input(
                    "Password", type="password", key="password_input"
                )

                if st.button("Login"):
                    # Initialize the database session
                    db = SessionLocal()

                    # Fetch the user from the database
                    user = get_user_by_username(username, db)

                    if user and user.password == password:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Incorrect username or password")

                    db.close()  # Close the session after use
            else:
                col = st.columns([2.5, 6, 1])
                with col[1]:
                    st.header(f"Welcome, {st.session_state.username}!")

                # Create a centered column
                col = st.columns([23, 30, 10])
                with col[1]:
                    if st.button("Logout"):
                        st.session_state.logged_in = False
                        st.session_state.username = None
                        st.rerun()

    except Exception as e:
        st.error("An error occured during login.")
