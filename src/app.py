# src/app.py
import streamlit as st
from cover_letter_generator import generate_cover_letter
from resume_customizer import customize_resume
from utils.helpers import insert_application
from datetime import datetime

def main():
    st.title('Job Search Helper')

    if 'form_key' not in st.session_state:
        st.session_state['form_key'] = 0
    unique_form_key = str(st.session_state['form_key'])

    if 'cover_letter_content' not in st.session_state:
        st.session_state['cover_letter_content'] = ""
    if 'resume_content' not in st.session_state:
        st.session_state['resume_content'] = ""

    # Job details input area
    job_title = st.text_input("Job Title:", key="job_title" + unique_form_key)
    company_name = st.text_input("Company Name:", key="company_name" + unique_form_key)
    job_location = st.text_input("Job Location:", key="job_location" + unique_form_key)
    salary = st.text_input("Salary (optional):", key="salary" + unique_form_key)
    job_description = st.text_area("📝 Paste the job description here:", height=300, key="job_description" + unique_form_key)

    # Position type and version selection
    position_type = st.selectbox("Select the position type:",
                                 ("Investment Analyst", "Fixed Income Analyst", "Data Analyst", "Data Scientist"),
                                 index=0, key="position_type" + unique_form_key)
    version = st.number_input("Enter the document version (leave 0 for the most recent):",
                              min_value=0, value=0, step=1, key="version" + unique_form_key)
    if version == 0:
        version = None

    # Generate Cover Letter button
    if st.button('Generate Cover Letter'):
        st.session_state['cover_letter_content'] = generate_cover_letter(job_description, position_type, version)
    
    # Customize Resume button
    if st.button('Customize Resume'):
        st.session_state['resume_content'] = customize_resume(job_description, position_type, version)
    
    # Display generated cover letter and resume
    if st.session_state['cover_letter_content']:
        st.text_area("Generated Cover Letter:", st.session_state['cover_letter_content'], height=300, key="cover_letter_display")
    
    if st.session_state['resume_content']:
        st.text_area("Customized Resume:", st.session_state['resume_content'], height=300, key="resume_display")

    # Insert into Database button
    if st.button('Insert into Database'):
        current_date = datetime.now().date()
        insert_application(
            application_date=current_date,
            job_title=job_title,
            company_name=company_name,
            job_location=job_location,
            document_id=None, 
            resume=st.session_state['resume_content'],
            cover_letter=st.session_state['cover_letter_content'] if st.session_state['cover_letter_content'] else None,
            salary=salary if salary else None 
        )
        st.success("Application documents inserted successfully.")

    if st.button('Clear'):
        st.session_state['form_key'] += 1
        st.session_state['cover_letter_content'] = ""
        st.session_state['resume_content'] = ""
        st.rerun()

if __name__ == '__main__':
    main()

