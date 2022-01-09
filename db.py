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

    def select_predict(self) -> None:
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

    def select_means(self) -> None:
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
                df = df[df.created_time == df.created_time.max()]
                df["IoU"] = 0.03
                df = df[["IoU", "ap", "precision", "recall"]]
                df = df.mean()

                return df
        finally:
            connection.close()
