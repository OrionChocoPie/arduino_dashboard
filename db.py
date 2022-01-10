import os

import psycopg2
from pandas import DataFrame
import pandas.io.sql as sqlio

api_key = os.getenv("API_KEY", "optional-default")


class Connector:
    DBNAME = os.getenv("DBNAME")
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT_SQL")

    select_values_query = """
        SELECT * FROM sensors
    """

    def select_values(self) -> None:
        connection = psycopg2.connect(
            user=self.USER,
            password=self.PASSWORD,
            host=self.HOST,
            port=self.PORT,
            database=self.DBNAME,
        )

        try:
            with connection:
                df = sqlio.read_sql_query(self.select_values_query, connection)

                return df
        finally:
            connection.close()
