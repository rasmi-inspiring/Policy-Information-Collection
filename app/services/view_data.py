import streamlit as st
from models import FileData, FormData
from sqlalchemy.orm import Session
from database import engine


def view_data_page():

    try:
        st.title("View Data")

        # Increase font size for the title
        st.markdown(
            "<h1 style='font-size: 32px;'>View Data</h1>", unsafe_allow_html=True
        )

        with Session(engine) as session:
            form_data_entries = session.query(FormData).all()
            st.subheader(f"Total Queries: {len(form_data_entries)}")

            for i, form_data in enumerate(form_data_entries, 1):
                with st.expander(f"## Query {i}: {form_data.query}"):

                    # Function to display key-value pairs without boxes and custom font size
                    def display_key_value(
                        key, value, inline=False, margin_bottom=10, font_size="16px"
                    ):

                        if value:
                            st.markdown(
                                f"<div style='margin-bottom: {margin_bottom}px; font-size: {font_size};'>"
                                f"<span style='font-weight: bold;'>{key}:</span> "
                                f"<span>{value}</span></div>",
                                unsafe_allow_html=True,
                            )

                    # Section 1: ID, Category and Offices
                    st.markdown(
                        "<h3 style='font-size: 24px;'>General Information</h3>",
                        unsafe_allow_html=True,
                    )

                    display_key_value(
                        "Category",
                        form_data.category,
                        margin_bottom=20,
                        font_size="18px",
                    )

                    col1, col2 = st.columns([1, 1])
                    with col1:
                        display_key_value(
                            "Related Office",
                            form_data.related_office,
                            margin_bottom=20,
                            font_size="18px",
                        )
                    with col2:
                        display_key_value(
                            "Secondary Office 1",
                            form_data.related_secondary_office_1,
                            margin_bottom=20,
                            font_size="18px",
                        )
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        display_key_value(
                            "Secondary Office 2",
                            form_data.related_secondary_office_2,
                            margin_bottom=20,
                            font_size="18px",
                        )
                    with col2:
                        display_key_value(
                            "Other Offices",
                            form_data.other_offices,
                            margin_bottom=20,
                            font_size="18px",
                        )
                    st.markdown("---")

                    # Section 2: Topic, Query, and Response
                    st.markdown(
                        "<h3 style='font-size: 24px;'>Details</h3>",
                        unsafe_allow_html=True,
                    )
                    display_key_value(
                        "Topic", form_data.topic, margin_bottom=20, font_size="18px"
                    )
                    display_key_value(
                        "Query", form_data.query, margin_bottom=20, font_size="18px"
                    )
                    display_key_value(
                        "Response",
                        form_data.response,
                        margin_bottom=20,
                        font_size="18px",
                    )
                    st.markdown("---")

                    st.markdown(
                        "<h3 style='font-size: 24px;'>Attachments & References</h3>",
                        unsafe_allow_html=True,
                    )
                    display_key_value(
                        "Attachments",
                        form_data.attachments,
                        margin_bottom=20,
                        font_size="18px",
                    )
                    display_key_value(
                        "Links", form_data.links, margin_bottom=20, font_size="18px"
                    )
                    display_key_value(
                        "Related Law/Policy/Act",
                        form_data.related_law_policy_act,
                        margin_bottom=20,
                        font_size="18px",
                    )

                    # Section 4: Validation Info
                    st.markdown("---")
                    st.markdown(
                        "<h3 style='font-size: 24px;'>Validated By</h3>",
                        unsafe_allow_html=True,
                    )
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        display_key_value(
                            "Name",
                            form_data.validated_by_name,
                            margin_bottom=20,
                            font_size="18px",
                        )
                    with col2:
                        display_key_value(
                            "Office",
                            form_data.validated_by_office,
                            margin_bottom=20,
                            font_size="18px",
                        )

                    col1, col2 = st.columns([1, 1])
                    with col1:
                        display_key_value(
                            "Position",
                            form_data.validated_by_position,
                            margin_bottom=20,
                            font_size="18px",
                        )
                    with col2:
                        display_key_value(
                            "Address",
                            form_data.validated_by_address,
                            margin_bottom=20,
                            font_size="18px",
                        )

                    st.markdown("---")

                    file_data_list = (
                        session.query(FileData)
                        .filter_by(form_data_id=form_data.id)
                        .all()
                    )
                    if file_data_list:
                        st.markdown(
                            "<h3 style='font-size: 24px;'>Uploaded Files</h3>",
                            unsafe_allow_html=True,
                        )
                        for file_data in file_data_list:
                            with open(file_data.file_path, "rb") as f:
                                file_bytes = f.read()

                            st.download_button(
                                label=f"Download {file_data.file_name}",
                                data=file_bytes,
                                file_name=file_data.file_name,
                                mime="application/octet-stream",
                                key=f"download_{file_data.id}",
                            )

    except Exception as e:
        st.error("An error occured while trying to load view data page.")
