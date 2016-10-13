import pickle
from announcements import *

# Load list of asx stocks.
database = DatabaseMySQL()
sql = "Select distinct company_id from company_announcements"
stock_codes = database.get_query_df(sql)
data = []
labels = []

print("Retrieved stock list..")

# Loop through stock list.
for stock in stock_codes['company_id']:

    print("Loading data for.. " + str(stock))

    # Load all announcements for this stock.
    sql = "Select * from company_announcements where raw <> '' and " \
          "company_id = " + str(stock) + \
          " order by published_at DESC"
    temp = database.get_query_df(sql)

    if len(temp) > 0:
        announcements = Announcements(temp)

        # Load the test data for the announcements for this stock.
        df = announcements.get_test_data()

        data += df[0]
        labels += df[1]

print("\nData loaded. Number of data points is: %0.2f" % len(labels))

# Save data so don't have to do this load every new analysis run.
pickle.dump(data, open('data.pkl', "wb"))
pickle.dump(labels, open('labels.pkl', "wb"))

print("\nData saved, ready for analysis.")
