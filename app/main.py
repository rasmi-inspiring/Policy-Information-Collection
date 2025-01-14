import streamlit as st

from services.login_func import login
from services.submit_form import submit_form_page
from services.view_data import view_data_page

from database import engine, Base
from sqlalchemy.exc import OperationalError
from models import FormData, FileData, User
import os


def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError as e:
        st.error(f"An error occured while running the application.")


# Set the page layout to 'wide'
st.set_page_config(page_title="Policy Data Collection", layout="wide")


def main_content():
    try:
        create_tables()
        st.title("Policy Data Collection")

        # Create tabs for different functionalities
        tabs = st.tabs(["Add Data", "View Data"])

        with tabs[0]:
            submit_form_page()

        with tabs[1]:
            view_data_page()

    except Exception as e:
        st.error("An error occured while trying to load the application.")


def main():
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            width: 400px;  /* Adjust the sidebar width */
            min-width: 400px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    login()

    if st.session_state.logged_in:
        main_content()
    else:
        st.markdown(
            """
            <style>
            .header {
                font-size: 70px;
                text-align: center;
                font-weight: bold;
                margin-top: 70px;
                margin-bottom: 20px;
            }
            .subheader {
                font-size: 25px;
                text-align: center;
                color: gray;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="header">Policy Data Collection</div>', unsafe_allow_html=True
        )
        st.markdown(
            '<div class="subheader">A platform to collect data related to different government services.</div>',
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
