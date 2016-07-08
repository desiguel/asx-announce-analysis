import netrc
import MySQLdb
import pandas as pd

class Database(object):
    """
    Sets up the database connection for use by the application
    """

    # Define which host in the .netrc file to use
    DBHOST = '192.168.23.3'
    DBNAME = "streamin_equities"

    # Read from my .netrc file.
    secrets = netrc.netrc()
    username, account, password = secrets.authenticators(DBHOST)

    connection = MySQLdb.connect(host=DBHOST, user=username, passwd=password,
                                 db=DBNAME)

    def get_cursor(self):
        cursor = self.connection.cursor()
        return cursor

    def get_connection(self):
        """Return database connection."""
        return self.connection

    def close_connection(self):
        self.connection.close()
        return

    def get_query_result(self, sql):
        df = pd.read_sql(sql, self.connection)
        return df
