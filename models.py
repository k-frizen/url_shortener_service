import sqlite3

DB_NAME = 'urls.db'
db_connection_factory = lambda: sqlite3.connect(DB_NAME)


def create_table():
    with db_connection_factory() as conn:
        conn.execute(
            """ 
            CREATE TABLE IF NOT EXISTS shorten_urls (
                original_url VARCHAR(255) PRIMARY KEY, 
                short_code VARCHAR(255) NOT NULL                
            )
            """
        )


def insert_short_url(short_code: str, original_url: str):
    with db_connection_factory() as conn:
        conn.execute("""
            INSERT INTO shorten_urls (short_code, original_url)
            VALUES (?, ?)
        """,
                     (short_code, original_url))


def delete_url(short_code: str):
    with db_connection_factory() as conn:
        conn.execute("""
            DELETE FROM shorten_urls
            WHERE short_code=?            
        """, short_code)
