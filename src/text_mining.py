from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from sklearn import cross_validation as cv
import numpy as np
from announcements import *

# Load list of asx stocks.
database = DatabaseMySQL()
sql = "Select distinct company_id from company_announcements"
stock_codes = database.get_query_df(sql)
data = []
labels = []

print("Retrieved stock list..")

# Loop thru stock list
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

print(labels)

# Transform the data - vectorise and apply tf-idf.
data = CountVectorizer().fit_transform(data)
tf_idf_transform = TfidfTransformer(use_idf=True).fit(data)
data = tf_idf_transform.transform(data)

# Splitting the data up into 60% training set, 20% cross-validation and 20% testing sets.
x_train, x_cv_test, y_train, y_cv_test = cv.train_test_split(data, labels, test_size=0.40, random_state=1)
x_cv, x_test, y_cv, y_test = cv.train_test_split(x_cv_test, y_cv_test, test_size=0.50, random_state=1)

# Test NB classifier
print("Running Naive Bayes classifier..")

classifier_nb = MultinomialNB().fit(x_train, y_train)
predicted = classifier_nb.predict(x_test)
accuracy = np.mean(predicted == y_test)

print("\nNaive Bayes model accuracy is: %0.2f" % accuracy)

print("\nRunning SVM classifier and tuning using grid search..\n")

# Grid search for best SVM parameters
cost_range = [1e-9, 1e-7, 1e-5, 1e-3, 0.1, 1, 100]
gamma_range = [1e-14, 1e-12, 1e-9, 1e-5, 0.1, 1]
parameters = dict(gamma=gamma_range, C=cost_range)
grid = GridSearchCV(SVC(), param_grid=parameters, cv=None, n_jobs=7)
grid.fit(x_train, y_train)

print("\nThe best SVM parameters are %s with a score of %0.2f"
      % (grid.best_params_, grid.best_score_))

predicted = grid.predict(x_test)
accuracy = np.mean(predicted == y_test)

print(metrics.classification_report(y_test, predicted))
print(metrics.confusion_matrix(y_test, predicted))

