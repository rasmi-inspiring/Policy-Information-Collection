import streamlit as st
from database import engine, Base
from sqlalchemy.exc import OperationalError
from models import FormData, FileData, User


def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError as e:
        st.error(f"An error occured while running the application.")


def is_quill_content_empty(html_content):
    """
    Check if Quill editor content is effectively empty
    Args:
        html_content (str): HTML content from Quill editor
    Returns:
        bool: True if content is empty, False otherwise
    """
    if not html_content:
        return True

    cleaned_content = html_content.replace("<p>", "").replace("</p>", "").strip()
    cleaned_content = cleaned_content.replace("<br>", "").replace("<br/>", "")

    return not bool(cleaned_content)


def validate_field(field_name, value="", show_error=False):
    """
    Validate a field and update its error state in the session
    Args:
        field_name (str): Name of the field to validate
        value (str): Value to check, defaults to empty string if using session state
        show_error (bool): Whether to show error messages
    Returns:
        bool: True if field is valid, False otherwise
    """
    if value == "":
        value = st.session_state.get(field_name, "")

    if field_name == "response":
        is_valid = not is_quill_content_empty(value)
    else:
        is_valid = value != ""

    st.session_state[f"{field_name}_error"] = not is_valid
    return is_valid
