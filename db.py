import psycopg2
from pandas import DataFrame
import pandas.io.sql as sqlio


class Connector:
    DBNAME = "postgres"
    USER = "postgres"
    PASSWORD = "wvHjfv6mN3KXUZZX"
    HOST = "database-1.cr2r5wsggaq4.us-east-2.rds.amazonaws.com"
    PORT = "5432"

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
