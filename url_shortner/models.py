import sqlite3

_DB_NAME = 'urls.db'
_db_connection_factory = lambda: sqlite3.connect(_DB_NAME)


def create_table():
    with _db_connection_factory() as conn:
        conn.execute(
            """ 
            CREATE TABLE IF NOT EXISTS shorten_urls (
                original_url VARCHAR(255) PRIMARY KEY, 
                short_code VARCHAR(255) NOT NULL                
            )
            """
        )


def insert_short_url(short_code: str, original_url: str):
    with _db_connection_factory() as conn:
        conn.execute("""
            INSERT INTO shorten_urls (short_code, original_url)
            VALUES (?, ?)
        """,
                     (short_code, original_url))


def delete_url(short_code: str):
    with _db_connection_factory() as conn:
        conn.execute("""
            DELETE FROM shorten_urls
            WHERE short_code=?            
        """, (short_code,))


def get_redirect_info(short_code: str) -> str | None:
    """Extract redirect data

    :param short_code: code to identify url"""
    with _db_connection_factory() as conn:
        redirect_data = conn.execute("""
                SELECT short_code FROM shorten_urls WHERE short_code=?
            """, (short_code,))
        return redirect_data.fetchone()


def is_unique_url(url: str) -> bool:
    """
        Check if a URL is unique in the database.

        This function queries the database to check if the provided URL exists
        as a shortened URL in the database. It returns True if the URL is unique
        (i.e., it doesn't exist in the database) and False otherwise.

        :param url: The URL to check for uniqueness.

        :returns: True if the URL is unique, False if it already exists in the database.
        """
    res = get_redirect_info(url)
    return not bool(res)
