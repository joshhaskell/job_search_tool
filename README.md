# Job Search Tool

This project was designed to be a job search assistance tool built with Python and Streamlit. The application allows users to generate tailored cover letters and customize resumes based on a job description and using context from their experience. 

## Features

- **Generate Cover Letter**: Automatically create a professional cover letter from a pasted job description.
- **Customize Resume**: Modify an existing resume to match the requirements of a job description.
- **Database Integration**: Save and manage job application documents within a PostgreSQL database.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository:**

```git clone https://github.com/joshhaskell/job_search_tool.git```

1. **Navigate to the project directory:**

```cd job_search_tool```

1. **Install the required Python packages:**

```pip install -r requirements.txt```

1. **Set up environment variables:**
Create a `.env` file in the root of the project and add your OpenAI API key and database credentials:

```DB_HOST = 'your_db_host'```
```DB_NAME = 'your_db_name'```
```DB_USER = 'your_db_user'```
```DB_PASSWORD = 'your_db_password'```
```DB_PORT = 'your_db_port'```
```OPENAI_API_KEY = 'your_openai_api_key'```

## Usage

To run the Streamlit application:

```streamlit run src/app.py```


This will start the Streamlit server, and you can view the app in your web browser.






