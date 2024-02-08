import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT")
    )

def create_tables():
    '''Create the documents and applications tables in the database.'''
    commands = (
        """
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            type VARCHAR(50),
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            version INTEGER,
            position_type VARCHAR(50)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS applications (
            id SERIAL PRIMARY KEY,
            job_title VARCHAR(255),
            company_name VARCHAR(255),
            job_location VARCHAR(255),
            application_date DATE,
            cover_letter_sample_doc_id INTEGER REFERENCES documents(id),
            resume_sample_doc_id INTEGER REFERENCES documents(id),
            status VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resume TEXT,
            cover_letter TEXT,
            salary VARCHAR(255)
        )
        """
    )
    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        # Create each table
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_document(doc_type, content):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO documents (type, content) VALUES (%s, %s) RETURNING id;", (doc_type, content))
    doc_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return doc_id

def get_sample_documents(doc_type, position_type, version=None):
    """Retrieve documents of a specific document and position type from the database.
       If version is not specified, retrieve the most recent version."""
    conn = connect_db()
    cur = conn.cursor()
    if version is not None:
        cur.execute("SELECT content FROM documents WHERE type = %s AND position_type = %s AND version = %s ORDER BY created_at DESC LIMIT 1;", (doc_type, position_type, version))
    else:
        cur.execute("SELECT content FROM documents WHERE type = %s AND position_type = %s ORDER BY version DESC, created_at DESC LIMIT 1;", (doc_type, position_type))
    document = cur.fetchone()
    cur.close()
    conn.close()
    return document[0] if document else None

def insert_application(application_date, job_title, company_name, job_location, cover_letter_sample_doc_id, resume_sample_doc_id, resume, cover_letter=None, salary=None):
    """Insert a new application into the applications table with additional job details."""
    conn = connect_db()
    cur = conn.cursor()
    query = """
    INSERT INTO applications (application_date, job_title, company_name, job_location, cover_letter_sample_doc_id, resume_sample_doc_id, resume, cover_letter, salary)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    cur.execute(query, (application_date, job_title, company_name, job_location, cover_letter_sample_doc_id, resume_sample_doc_id, resume, cover_letter, salary))
    conn.commit()
    cur.close()
    conn.close()

