#!/usr/bin/python3
from database_mysql import DatabaseMySQL
import pandas as pd


class Stock(object):
    """
    Contains the meta-data for an ASX stock.
    """

    def __init__(self, company_id):
        """
        Return a Announcement object.
        """
        self.company_id = company_id

    def get_asx_code(self):
        """
        Return the stock code associated with this stock.
        :return: a string containing the ASX code
        """
        # Connect to the database and return cursor
        database = DatabaseMySQL()

        # Query database.
        sql = "Select short_name from companies where id =" + str(self.company_id)
        df = database.get_query_df(sql)
        code = df.iloc[0, 0]

        return code

    def get_price_history(self):
        """
        Return the price history of this stock.
        :return: A dataframe containing the price history.
        """
        # Connect to the database and return cursor
        database = DatabaseMySQL()

        # Query database.
        sql = "Select published_at, `close` from company_price_volume_history  \
               where company_id =" + str(self.company_id)
        df = database.get_query_df(sql)

        return df
