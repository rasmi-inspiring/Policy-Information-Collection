import streamlit as st
import os
from services.login_func import login
from services.submit_form import submit_form_page
from services.view_data import view_data_page
from services.edit_data import edit_data_page
from utils.helpers import create_tables, hide_anchor_link

# Set the page layout to 'wide'
st.set_page_config(page_title="Policy Data Collection", layout="wide")


def main_content():
    try:
        tab1, tab2, tab3 = st.tabs(["Add Data", "View Data", "Edit Data"])

        with tab1:
            submit_form_page()

        with tab2:
            view_data_page()

        with tab3:
            edit_data_page()

    except Exception as e:
        st.error(f"An error occurred while loading the main content.")


def main():
    os.makedirs("uploads", exist_ok=True)

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
    create_tables()
    hide_anchor_link()
    main()
