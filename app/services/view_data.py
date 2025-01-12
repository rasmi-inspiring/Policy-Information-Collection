import streamlit as st
from models import FileData, FormData
from sqlalchemy.orm import Session
from database import engine


# View Data Page
def view_data_page():
    st.title("View Data")
    with Session(engine) as session:
        form_data_entries = session.query(FormData).all()
        st.subheader(f"Total Queries: {len(form_data_entries)}")

        for i, form_data in enumerate(form_data_entries, 1):
            with st.expander(f"Query {i}: {form_data.query}"):
                st.write(f"**ID**: {form_data.id}")
                st.write(f"**Category**: {form_data.category}")
                st.write(f"**Related Office**: {form_data.related_office}")
                st.write(
                    f"**Related Secondary Office 1**: {form_data.related_secondary_office_1}"
                )
                st.write(
                    f"**Related Secondary Office 2**: {form_data.related_secondary_office_2}"
                )
                st.write(f"**Other Offices**: {form_data.other_offices}")
                st.write(f"**Topic**: {form_data.topic}")
                st.write(f"**Query**: {form_data.query}")
                st.write(f"**Response**:")
                st.markdown(form_data.response, unsafe_allow_html=True)
                st.write(f"**Attachments**: {form_data.attachments}")
                st.write(f"**Links**: {form_data.links}")
                st.write(
                    f"**Related Law/Policy/Act**: {form_data.related_law_policy_act}"
                )
                st.write(f"**Validated By Name**: {form_data.validated_by_name}")
                st.write(f"**Validated By Office**: {form_data.validated_by_office}")
                st.write(
                    f"**Validated By Position**: {form_data.validated_by_position}"
                )
                st.write(f"**Validated By Address**: {form_data.validated_by_address}")

                file_data_list = (
                    session.query(FileData).filter_by(form_data_id=form_data.id).all()
                )
                if file_data_list:
                    st.write("**Uploaded Files:**")
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
