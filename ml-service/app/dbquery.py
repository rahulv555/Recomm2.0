import os
import psycopg2

# DB connection configuration (can be overridden via environment variables)
DB_HOST = os.getenv("DB_HOST", "reco-postgres")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "reco_db")
DB_USER = os.getenv("DB_USER", "reco_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "reco_pass")


def execute_db_query(query, params=None):
    conn = None
    results = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        with conn.cursor() as cur:
            # Pass params here to handle the vector_list safely
            cur.execute(query, params)
            
            if cur.description:
                results = cur.fetchall()
            
            conn.commit()
    except Exception as e:
        print(f"Database error: {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()
    return results