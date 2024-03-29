# src/resume_customizer.py
import os
from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate 
from utils.helpers import get_sample_documents

# Set the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

def customize_resume(job_description, position_type, version=None):
    """Customizes a resume based on the job description, selected position type, and optionally a specific version."""

    context_info = {
        "Investment Analyst": "Focus on financial markets, investment strategies, and analytical skills.",
        "Fixed Income Analyst": "Emphasize understanding of bond markets, credit analysis, and income-generating investments.",
        "Data Analyst": "Highlight data processing, statistical analysis, and insight generation capabilities.",
        "Data Scientist": "Stress on advanced analytical techniques, machine learning, and data modeling skills."
    }

    # Select the context information based on the position type
    selected_context = context_info.get(position_type, "")

    # Retrieve sample resume for additional context
    additional_context = get_sample_documents("resume", position_type)

    llm = OpenAI(api_key=openai_api_key)
    prompt_template = "Given the role of {position_type} requiring {context_info}, please write and adjust my resume based on the following job description:\n{job_description}\n\nSample Resume:\n{additional_context}"
    prompt = PromptTemplate(
        input_variables=["position_type", "context_info", "job_description", "additional_context"], 
        template=prompt_template
    )

    # Initialize the LLMChain with the llm instance, inputs and generating the response
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    inputs = {
        "position_type": position_type,
        "context_info": selected_context,
        "job_description": job_description,
        "additional_context": additional_context
    }
    response = llm_chain.invoke(input=inputs, temperature=0.2, return_only_outputs=True)
    return response['text'].strip()