#!/usr/bin/python3

from announcements import Announcements
from database import Database
from sklearn import cross_validation

# Load list of asx stocks.
database = Database()
fn_result = database.get_query_result("")
sql = "Select distinct company_id from company_announcements"
stock_codes = database.get_query_result(sql)

train_split = 0.6
test_split = 1 - train_split

# Loop thru stock list
for stock in stock_codes['company_id']:
    if stock == 1045:  # temporary.. for testing only

        # Load all announcements for this stock.
        sql = "Select * from company_announcements where " \
              "company_id = " + str(stock) + \
              " order by published_at DESC"
        temp = database.get_query_result(sql)
        announcements = Announcements(temp)

        # Load the test data for the announcements for this stock.
        df = announcements.get_test_data()

        # TODO Split the dataset into training and testing sets.
        # TODO Research on dealing with more features than observations.
        # TODO Possibly reduce features by using PCA.

        skf = cross_validation.StratifiedKFold(df[''], n_folds=2)

        for train_index, test_index in skf:
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]



        x_train = df.loc[:25000, 'review'].values
        y_train = df.loc[:25000, 'sentiment'].values
        x_test = df.loc[25000:, 'review'].values
        y_test = df.loc[25000:, 'sentiment'].values


    # TODO Run machine learning
    # TODO Probably use SVM


    # TODO Output results


# End loop

