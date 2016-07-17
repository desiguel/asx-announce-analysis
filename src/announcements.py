import datetime
from announcement import *


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

        for index, row in self.df.iterrows():

            if index == 0:
                last_date = row['published_at']

            if row['price_sens'] == 1:
                self.df.set_value(index, 'pre_sens', -1)
                last_ps_date = row['published_at']
                ps_counter += 1
                continue

            days_since_last_ps = (last_ps_date - row['published_at']).days
            sens_day_group = days_since_last_ps // self.pre_sens_days
            early_group = (last_date - row['published_at']).days // self.pre_sens_days

            if sens_day_group == 0:
                self.df.set_value(index, 'pre_sens', 1)
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
        result = []
        entry = []
        last_group = 0
        last_label = 0

        # Make sure the pre sens flag has been populated.
        self.add_pre_sens_flag()

        # Remove all ps announcements from dataframe
        announcements = self.df.drop(self.df[self.df.pre_sens == -1].index)

        for index, row in announcements.iterrows():

            # Initialise the 'last' values.
            if index == 0:
                last_group = row['pre_sens_counter']
                last_label = row['price_sens']

            # Set values for later processing.
            group = row['pre_sens_counter']
            label = row['pre_sens']

            # Get text data for this item.
            announcement = Announcement(row['company_id'], row['published_at'], row['price_sens'],
                                        row['price_sens'], row['link'])
            text = announcement.get_text_list(source)

            # Combine new data onto entry or push entry to array.
            if group != last_group or label != last_label:
                # push the last entry onto result
                if entry:
                    result.append(entry)
                # clear out entry and start new one.
                entry = [text, row['pre_sens']]
            else:
                # Update
                entry[0].extend(text)
                # entry = [new_entry, row['pre_sens']]

            last_group = group
            last_label = label

        # Update for last group
        result.append(entry)

        return result

    def get_announcements(self):
        self.add_pre_sens_flag()
        # print(self.df)
        return self.df
