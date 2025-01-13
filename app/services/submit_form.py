import os
import streamlit as st

from streamlit_quill import st_quill
from models import FileData, FormData
from database import SessionLocal


# Streamlit pages
def submit_form_page():
    # Base directory for file uploads
    APP_DIR = "app"
    UPLOAD_DIR = os.path.join(APP_DIR, "uploads")
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    st.title("Add Data")

    # Form fields
    st.subheader("Category")
    category = st.selectbox("", ["Government", "Non-Government", "Others"])
    if st.session_state.get("category") == "":
        st.session_state["category_error"] = True
    else:
        st.session_state["category_error"] = False

    # Related Offices Section
    st.subheader("Related Offices")
    related_office = st.text_input("Primary Office *", key="related_office")
    if st.session_state.get("related_office") == "":
        st.session_state["related_office_error"] = True
    else:
        st.session_state["related_office_error"] = False

    related_secondary_office_1 = st.text_input(
        "Secondary Office 1 (optional)", key="related_secondary_office_1"
    )
    if st.session_state.get("related_secondary_office_1") == "":
        st.session_state["related_secondary_office_1_error"] = True
    else:
        st.session_state["related_secondary_office_1_error"] = False

    related_secondary_office_2 = st.text_input(
        "Secondary Office 2 (optional)", key="related_secondary_office_2"
    )
    if st.session_state.get("related_secondary_office_2") == "":
        st.session_state["related_secondary_office_2_error"] = True
    else:
        st.session_state["related_secondary_office_2_error"] = False

    other_offices = st.text_area("Other Offices (optional)", key="other_offices")
    if st.session_state.get("other_offices") == "":
        st.session_state["other_offices_error"] = True
    else:
        st.session_state["other_offices_error"] = False

    # Topic and Query Section
    st.subheader("Topic and Query")
    topic = st.text_input("Topic *", key="topic")
    if st.session_state.get("topic") == "":
        st.session_state["topic_error"] = True
    else:
        st.session_state["topic_error"] = False

    query = st.text_area("Query *", key="query")
    if st.session_state.get("query") == "":
        st.session_state["query_error"] = True
    else:
        st.session_state["query_error"] = False

    # Response Section
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
    if st.session_state.get("response") == "":
        st.session_state["response_error"] = True
    else:
        st.session_state["response_error"] = False

    # Files, Attachments & Links Section
    st.subheader("Files, Attachments & Links")
    uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True)

    attachments = st.text_area("Attachments (optional)", key="attachments")
    if st.session_state.get("attachments") == "":
        st.session_state["attachments_error"] = True
    else:
        st.session_state["attachments_error"] = False

    links = st.text_area("Links (optional)", key="links")
    if st.session_state.get("links") == "":
        st.session_state["links_error"] = True
    else:
        st.session_state["links_error"] = False

    related_law_policy_act = st.text_area(
        "Related Law/Policy/Act (optional)", key="related_law_policy_act"
    )
    if st.session_state.get("related_law_policy_act") == "":
        st.session_state["related_law_policy_act_error"] = True
    else:
        st.session_state["related_law_policy_act_error"] = False

    # Validated By Section
    st.subheader("Validated By")
    validated_by_name = st.text_input("Name *", key="validated_by_name")
    if st.session_state.get("validated_by_name") == "":
        st.session_state["validated_by_name_error"] = True
    else:
        st.session_state["validated_by_name_error"] = False

    validated_by_office = st.text_input("Office *", key="validated_by_office")
    if st.session_state.get("validated_by_office") == "":
        st.session_state["validated_by_office_error"] = True
    else:
        st.session_state["validated_by_office_error"] = False

    validated_by_position = st.text_input("Position *", key="validated_by_position")
    if st.session_state.get("validated_by_position") == "":
        st.session_state["validated_by_position_error"] = True
    else:
        st.session_state["validated_by_position_error"] = False

    validated_by_address = st.text_area("Address *", key="validated_by_address")
    if st.session_state.get("validated_by_address") == "":
        st.session_state["validated_by_address_error"] = True
    else:
        st.session_state["validated_by_address_error"] = False

    # Check for errors before submission
    if st.button("Submit Form"):
        if any(
            field in st.session_state and st.session_state[field] == ""
            for field in [
                "related_office",
                "topic",
                "query",
                "response",
                "validated_by_name",
                "validated_by_office",
                "validated_by_position",
                "validated_by_address",
            ]
        ):
            st.error("Please fill all required fields.")
        else:
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

                # Handle file uploads
                for uploaded_file in uploaded_files:
                    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
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
