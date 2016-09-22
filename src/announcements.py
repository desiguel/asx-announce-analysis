import datetime
from announcement import *
from pricing import *
import pandas as pd


class Announcements(object):
    """
    Contains a list of announcements for a single stock.
    """

    def __init__(self, df):
        """
        Return a Announcement object.
        """
        self.df = df.copy(deep=True)
        self.pre_sens_days = 91

    def __iter__(self):
        return iter(self.df)

    def add_pre_sens_flag(self):
        """
        Adds a column to the dataframe that provides a flag as to whether an announcement
        is in the pre-price sensitive zone.
        1 in a pre-sensitive announcement zone
        0 not in a pre-sensitive announcement zone
        -1 not useful for analysis
        """
        # Add default
        self.df['pre_sens'] = -1
        self.df['pre_sens_counter'] = 0

        last_date = datetime.datetime.strptime('01012000', "%d%m%Y")
        last_ps_date = datetime.datetime.strptime('01012000', "%d%m%Y")
        ps_counter = 0
        non_ps_counter = 1
        last_sens_day_group = 0
        price_result_sign = 0

        for index, row in self.df.iterrows():

            if index == 0:
                last_date = row['published_at']

            if row['price_sens'] == 1:
                self.df.set_value(index, 'pre_sens', -1)
                last_ps_date = row['published_at']
                ps_counter += 1
                price_result_sign = get_price_sign(row['company_id'], last_ps_date)
                continue

            days_since_last_ps = (last_ps_date - row['published_at']).days
            sens_day_group = days_since_last_ps // self.pre_sens_days
            early_group = (last_date - row['published_at']).days // self.pre_sens_days

            if sens_day_group == 0:
                self.df.set_value(index, 'pre_sens', 1 + price_result_sign)
                self.df.set_value(index, 'pre_sens_counter', ps_counter)
            else:
                if early_group > 0:
                    self.df.set_value(index, 'pre_sens', 0)

                    if sens_day_group != last_sens_day_group:
                        non_ps_counter += 1

                    self.df.set_value(index, 'pre_sens_counter', non_ps_counter)

            last_sens_day_group = sens_day_group

        return

    def get_test_data(self, source="html"):
        """
        Condenses the announcements dataframe into a test data-set.
        Assumes that the pre_sens_flag has already been added.
        """

        # An an array of arrays containing a word list and a label.
        # So [[['one','two',...,'nine'], 0] .. ]

        # Make sure the pre sens flag has been populated.
        self.add_pre_sens_flag()

        # Remove all ps announcements from dataframe
        announcements = self.df.drop(self.df[self.df.pre_sens == -1].index)

        # Group by and join
        def f(x):
            return pd.Series(dict(corpora=' '.join(x['raw'])))

        df = announcements.groupby(['pre_sens', 'pre_sens_counter']).apply(f).reset_index()
        df = df.drop('pre_sens_counter', 1)

        return df['corpora'].tolist(), df['pre_sens'].tolist()

    def get_announcements(self):
        self.add_pre_sens_flag()
        # print(self.df)
        return self.df