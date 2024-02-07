# src/app.py
import streamlit as st
from cover_letter_generator import generate_cover_letter
from resume_customizer import customize_resume
from utils.scraper import scrape_job_description

def main():
    st.title('Job Search Helper')

    # Option for user to select input type
    #TODO: Add support for URL input
    input_type = st.radio("Choose how to input the job description:",
                          ('Paste Text', 'Enter URL'))


    job_description = ""
    if input_type == 'Enter URL':
        job_url = st.text_input("Enter the job posting URL:", "")
        if st.button('Fetch Job Description'):
            job_description = scrape_job_description(job_url)
            st.text_area("Fetched Job Description:", job_description, height=300)
    else:
        job_description = st.text_area("Paste the job description here:", height=300)

    position_type = st.selectbox(
        "Select the position type:",
        ("Investment Analyst", "Fixed Income Analyst", "Data Analyst", "Data Scientist"),
        index=0
    )

    # After selecting the position type, add an option to select the document version
    version = st.number_input("Enter the document version (leave 0 for the most recent):", min_value=0, value=0, step=1)
    if version == 0:
        version = None

    if job_description:
        if st.button('Generate Cover Letter'):
            cover_letter = generate_cover_letter(job_description, position_type, version)
            st.text_area("Generated Cover Letter:", cover_letter, height=300)
        
        if st.button('Customize Resume'):
            customized_resume = customize_resume(job_description, position_type, version)
            st.text_area("Customized Resume:", customized_resume, height=300)

if __name__ == '__main__':
    main()

