import netrc
import MySQLdb


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

    def close_connection(self):
        self.connection.close()
        return
