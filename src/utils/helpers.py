import psycopg2
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

def insert_application(application_date, job_title, company_name, job_location, document_id, resume, cover_letter=None, salary=None):
    """Insert a new application into the applications table with additional job details."""
    conn = connect_db()
    cur = conn.cursor()
    query = """
    INSERT INTO applications (application_date, job_title, company_name, job_location, document_id, resume, cover_letter, salary)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    cur.execute(query, (application_date, job_title, company_name, job_location, document_id, resume, cover_letter, salary))
    conn.commit()
    cur.close()
    conn.close()

