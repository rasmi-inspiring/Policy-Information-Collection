import os
import streamlit as st
from streamlit_quill import st_quill
from connection.models import FileData, FormData
from connection.database import SessionLocal


def edit_data_page():
    try:
        st.title("Edit Data")

        # Initialize session state for storing form data if not already present
        if "form_data" not in st.session_state:
            st.session_state.form_data = {}
            st.session_state.selected_query_id = None
            st.session_state.show_form = False

        # Select query to edit
        with SessionLocal() as session:
            queries = session.query(FormData).order_by(FormData.id.desc()).all()
            query_options = {f"{q.id} - {q.query}": q.id for q in queries}
            selected_query = st.selectbox(
                "Select a Query to Edit",
                options=list(query_options.keys()),
                key="query_selector",
            )

        # Handle "Update Selected Query" button click
        if st.button("Update Selected Query") or st.session_state.show_form:
            st.session_state.show_form = True
            query_id = query_options[selected_query]

            # Only fetch data if we're selecting a new query or haven't loaded data yet
            if st.session_state.selected_query_id != query_id:
                with SessionLocal() as session:
                    query_data = (
                        session.query(FormData).filter(FormData.id == query_id).first()
                    )
                    # Get associated files
                    files = (
                        session.query(FileData)
                        .filter(FileData.form_data_id == query_id)
                        .all()
                    )

                    if query_data:
                        st.session_state.form_data = {
                            "category": query_data.category,
                            "related_office": query_data.related_office,
                            "related_secondary_office_1": query_data.related_secondary_office_1,
                            "related_secondary_office_2": query_data.related_secondary_office_2,
                            "other_offices": query_data.other_offices,
                            "topic": query_data.topic,
                            "query": query_data.query,
                            "response": query_data.response,
                            "attachments": query_data.attachments,
                            "links": query_data.links,
                            "related_law_policy_act": query_data.related_law_policy_act,
                            "validated_by_name": query_data.validated_by_name,
                            "validated_by_office": query_data.validated_by_office,
                            "validated_by_position": query_data.validated_by_position,
                            "validated_by_address": query_data.validated_by_address,
                            "existing_files": files,
                        }
                st.session_state.selected_query_id = query_id

            # Form Fields
            st.subheader("Category")

            category = st.selectbox(
                "",
                ["Government", "Non-Government", "Others"],
                index=["Government", "Non-Government", "Others"].index(
                    st.session_state.form_data.get("category", "Government")
                ),
                key="category_selector",  # Add this line
            )

            st.subheader("Related Offices")
            col1, col2 = st.columns(2)

            with col1:
                related_office = st.text_input(
                    "Primary Office",
                    value=st.session_state.form_data.get("related_office", ""),
                )
                related_secondary_office_1 = st.text_input(
                    "Secondary Office 1 (optional)",
                    value=st.session_state.form_data.get(
                        "related_secondary_office_1", ""
                    ),
                )
            with col2:
                related_secondary_office_2 = st.text_input(
                    "Secondary Office 2 (optional)",
                    value=st.session_state.form_data.get(
                        "related_secondary_office_2", ""
                    ),
                )
                other_offices = st.text_input(
                    "Other Offices (optional)",
                    value=st.session_state.form_data.get("other_offices", ""),
                )

            st.subheader("Topic and Query")
            col1, col2 = st.columns(2)
            with col1:
                topic = st.text_input(
                    "Topic",
                    value=st.session_state.form_data.get("topic", ""),
                )
            with col2:
                query = st.text_area(
                    "Query",
                    value=st.session_state.form_data.get("query", ""),
                    height=100,
                )

            st.subheader("Response")
            response = st_quill(
                value=st.session_state.form_data.get("response", ""),
                html=True,
                toolbar=[
                    ["bold", "italic", "underline", "strike"],
                    ["blockquote", "code-block"],
                    [{"header": 1}, {"header": 2}],
                    [{"list": "ordered"}, {"list": "bullet"}],
                    ["link", "image"],
                    ["clean"],
                ],
            )

            st.subheader("Files, Attachments & Links")

            # Display existing files with delete buttons
            if st.session_state.form_data.get("existing_files"):
                st.write("Existing Files:")
                for file in st.session_state.form_data["existing_files"]:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.text(file.file_name)
                    with col2:
                        delete_button = st.button(
                            "Delete File",
                            key=f"delete_{file.id}",
                            type="primary",
                            help="Click to delete this file",
                            use_container_width=True,
                        )

                        st.markdown(
                            f"""
                            <style>
                                div[data-testid="stButton"] button[kind="primary"][data-testid="delete_{file.id}"] {{
                                    background-color: #FF4B4B;
                                    color: white;
                                }}
                            </style>
                            """,
                            unsafe_allow_html=True,
                        )

                        if delete_button:
                            try:
                                with SessionLocal() as session:
                                    file_to_delete = session.query(FileData).get(
                                        file.id
                                    )
                                    if file_to_delete:
                                        # Delete physical file
                                        if os.path.exists(file_to_delete.file_path):
                                            os.remove(file_to_delete.file_path)
                                        # Delete database record
                                        session.delete(file_to_delete)
                                        session.commit()
                                        st.success(
                                            f"File '{file.file_name}' has been deleted successfully!"
                                        )
                                        # Update session state
                                        st.session_state.form_data["existing_files"] = [
                                            f
                                            for f in st.session_state.form_data[
                                                "existing_files"
                                            ]
                                            if f.id != file.id
                                        ]
                                        st.rerun()
                            except Exception as e:
                                st.error(f"Error deleting file.")

            # File uploader for new files
            uploaded_files = st.file_uploader(
                "Upload New Files",
                accept_multiple_files=True,
            )

            col1, col2, col3 = st.columns(3)
            with col1:
                attachments = st.text_area(
                    "Attachments (optional)",
                    value=st.session_state.form_data.get("attachments", ""),
                    height=150,
                )
            with col2:
                links = st.text_area(
                    "Links (optional)",
                    value=st.session_state.form_data.get("links", ""),
                    height=150,
                )
            with col3:
                related_law_policy_act = st.text_area(
                    "Related Law/Policy/Act (optional)",
                    value=st.session_state.form_data.get("related_law_policy_act", ""),
                    height=150,
                )

            st.subheader("Validated By")
            col1, col2 = st.columns(2)
            with col1:
                validated_by_name = st.text_input(
                    "Name",
                    value=st.session_state.form_data.get("validated_by_name", ""),
                )
                validated_by_office = st.text_input(
                    "Office",
                    value=st.session_state.form_data.get("validated_by_office", ""),
                )
            with col2:
                validated_by_position = st.text_input(
                    "Position",
                    value=st.session_state.form_data.get("validated_by_position", ""),
                )
                validated_by_address = st.text_input(
                    "Address",
                    value=st.session_state.form_data.get("validated_by_address", ""),
                )

            # Update button at the end
            if st.button("Update Data"):
                with SessionLocal() as session:
                    form_data = (
                        session.query(FormData)
                        .filter(FormData.id == st.session_state.selected_query_id)
                        .first()
                    )

                    if form_data:
                        # Update form fields
                        form_data.category = category
                        form_data.related_office = related_office
                        form_data.related_secondary_office_1 = (
                            related_secondary_office_1
                        )
                        form_data.related_secondary_office_2 = (
                            related_secondary_office_2
                        )
                        form_data.other_offices = other_offices
                        form_data.topic = topic
                        form_data.query = query
                        form_data.response = response
                        form_data.attachments = attachments
                        form_data.links = links
                        form_data.related_law_policy_act = related_law_policy_act
                        form_data.validated_by_name = validated_by_name
                        form_data.validated_by_office = validated_by_office
                        form_data.validated_by_position = validated_by_position
                        form_data.validated_by_address = validated_by_address

                        # Handle new file uploads
                        if uploaded_files:
                            for uploaded_file in uploaded_files:
                                file_path = os.path.join(
                                    os.getcwd(), "uploads", uploaded_file.name
                                )
                                with open(file_path, "wb") as f:
                                    f.write(uploaded_file.getbuffer())

                                file_data = FileData(
                                    file_name=uploaded_file.name,
                                    file_path=file_path,
                                    form_data_id=form_data.id,
                                )
                                session.add(file_data)

                        session.commit()
                        st.success("Data updated successfully!")

                        # Reset form state
                        st.session_state.show_form = False
                        st.session_state.selected_query_id = None
                        st.session_state.form_data = {}

                        # Refresh the page
                        st.rerun()

    except Exception as e:
        st.error(f"An error occurred while loading the edit data page.")
