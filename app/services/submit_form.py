import os
import streamlit as st
from streamlit_quill import st_quill
from models import FileData, FormData
from database import SessionLocal

from services.utils import is_quill_content_empty, validate_field


def submit_form_page():
    try:
        st.title("Add Data")

        with st.container():
            # Category Section
            st.subheader("Category")
            category = st.selectbox("", ["Government", "Non-Government", "Others"])
            validate_field("category", category)

        # Related Offices Section
        with st.container():
            st.subheader("Related Offices")
            col1, col2 = st.columns(2)

            with col1:
                related_office = st.text_input("Primary Office *", key="related_office")
                validate_field("related_office")
                related_secondary_office_1 = st.text_input(
                    "Secondary Office 1 (optional)", key="related_secondary_office_1"
                )
                validate_field("related_secondary_office_1")

            with col2:
                related_secondary_office_2 = st.text_input(
                    "Secondary Office 2 (optional)", key="related_secondary_office_2"
                )
                validate_field("related_secondary_office_2")
                other_offices = st.text_input(
                    "Other Offices (optional)", key="other_offices"
                )
                validate_field("other_offices")

        # Topic and Query Section
        with st.container():
            st.subheader("Topic and Query")
            col1, col2 = st.columns(2)

            with col1:
                topic = st.text_input("Topic *", key="topic")
                validate_field("topic")

            with col2:
                query = st.text_area("Query *", key="query", height=100)
                validate_field("query")

        # Response Section
        with st.container():
            st.subheader("Response *")
            response = st_quill(
                html=True,
                toolbar=[
                    ["bold", "italic", "underline", "strike"],
                    ["blockquote", "code-block"],
                    [{"header": 1}, {"header": 2}],
                    [{"list": "ordered"}, {"list": "bullet"}],
                    ["link", "image"],
                    ["clean"],
                ],
                placeholder="Start typing here...",
            )

        # Files, Attachments & Links Section
        with st.container():
            st.subheader("Files, Attachments & Links")

            uploaded_files = st.file_uploader(
                "Upload Files", accept_multiple_files=True
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                attachments = st.text_area(
                    "Attachments (optional)", key="attachments", height=150
                )
                validate_field("attachments")

            with col2:
                links = st.text_area("Links (optional)", key="links", height=150)
                validate_field("links")

            with col3:
                related_law_policy_act = st.text_area(
                    "Related Law/Policy/Act (optional)",
                    key="related_law_policy_act",
                    height=150,
                )
                validate_field("related_law_policy_act")

        # Validated By Section
        with st.container():
            st.subheader("Validated By")
            col1, col2 = st.columns(2)

            with col1:
                validated_by_name = st.text_input("Name *", key="validated_by_name")
                validate_field("validated_by_name")
                validated_by_office = st.text_input(
                    "Office *", key="validated_by_office"
                )
                validate_field("validated_by_office")

            with col2:
                validated_by_position = st.text_input(
                    "Position *", key="validated_by_position"
                )
                validate_field("validated_by_position")
                validated_by_address = st.text_input(
                    "Address *", key="validated_by_address"
                )
                validate_field("validated_by_address")

        # Submit button with some spacing
        st.write("")
        if st.button("Submit Form"):
            # Get current values for required fields
            required_fields = {
                "related_office": related_office,
                "topic": topic,
                "query": query,
                "response": response,
                "validated_by_name": validated_by_name,
                "validated_by_office": validated_by_office,
                "validated_by_position": validated_by_position,
                "validated_by_address": validated_by_address,
            }

            # Check all required fields including response
            validation_failed = False
            error_messages = []

            # Special check for response field
            if is_quill_content_empty(response):
                error_messages.append("Response field cannot be empty")
                validation_failed = True

            # Check other required fields
            empty_fields = [
                field
                for field, value in required_fields.items()
                if field != "response" and not value
            ]

            if empty_fields:
                error_messages.append(f"Please fill all required fields.")
                validation_failed = True

            if validation_failed:
                for error in error_messages:
                    st.error(error)
                return

            try:
                # Save data to the database
                with SessionLocal() as session:
                    form_data = FormData(
                        category=category,
                        related_office=related_office,
                        related_secondary_office_1=related_secondary_office_1,
                        related_secondary_office_2=related_secondary_office_2,
                        other_offices=other_offices,
                        topic=topic,
                        query=query,
                        response=response,
                        attachments=attachments,
                        links=links,
                        related_law_policy_act=related_law_policy_act,
                        validated_by_name=validated_by_name,
                        validated_by_office=validated_by_office,
                        validated_by_position=validated_by_position,
                        validated_by_address=validated_by_address,
                    )

                    session.add(form_data)
                    session.commit()

                    for uploaded_file in uploaded_files:
                        file_path = os.path.join(
                            os.getcwd(), "uploads", uploaded_file.name
                        )
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)

                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        file_data = FileData(
                            file_name=uploaded_file.name,
                            file_path=file_path,
                            form_data_id=form_data.id,
                        )
                        session.add(file_data)

                    session.commit()

                    st.success("Form submitted successfully!")

            except Exception as e:
                st.error(f"Error saving the data.")
                session.rollback()

    except Exception as e:
        st.error(f"An error occurred while loading the form.")
