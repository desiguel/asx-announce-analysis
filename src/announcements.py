import pandas as pd
import datetime


class Announcements(object):
    """
    Contains a list of announcements for a single stock.
    """

    def __init__(self, df):
        """
        Return a Announcement object.
        """
        self.df = df
        self.pre_sens_days = 91

    def __add_pre_sens_flag(self):
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

        last_ps_date = datetime.datetime.strptime('01012010', "%d%m%Y")
        ps_counter = 0
        non_ps_counter = 0
        last_sens_day_group = 0

        for index, row in self.df.iterrows():

            if row['price_sens'] == 1:
                self.df.set_value(index, 'pre_sens', -1)
                last_ps_date = row['published_at']
                ps_counter += 1
                continue

            days_since_last_ps = (last_ps_date - row['published_at']).days
            sens_day_group = days_since_last_ps // self.pre_sens_days

            if sens_day_group == 0:
                self.df.set_value(index, 'pre_sens', 1)
                self.df.set_value(index, 'pre_sens_counter', ps_counter)
            else:
                self.df.set_value(index, 'pre_sens', 0)

                if sens_day_group != last_sens_day_group:
                    non_ps_counter += 1

                self.df.set_value(index, 'pre_sens_counter', non_ps_counter)

            last_sens_day_group = sens_day_group

        return

    def get_announcements(self):
        self.__add_pre_sens_flag()
        print(self.df)
        return self.df
