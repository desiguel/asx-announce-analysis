from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.grid_search import GridSearchCV
from sklearn import cross_validation as cv
import numpy as np
from announcements import *

# Load list of asx stocks.
database = DatabaseMySQL()
sql = "Select distinct company_id from company_announcements"
stock_codes = database.get_query_df(sql)
data = []
labels = []

print("Retreived stock list..")

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

# Splitting the data up into 60% training set, 20% cross-validation and 20% testing sets.
x_train, x_cv_test, y_train, y_cv_test = cv.train_test_split(data, labels, test_size=0.40, random_state=1)
x_cv, x_test, y_cv, y_test = cv.train_test_split(x_cv_test, y_cv_test, test_size=0.50, random_state=1)

# print("Running Naive Bayes classifier..")
#
# text_clf = Pipeline([('vect', CountVectorizer()),
#                      ('tfidf', TfidfTransformer()),
#                      ('clf', MultinomialNB()),
#                      ])
#
# text_clf = text_clf.fit(x_train, y_train)
#
# predicted = text_clf.predict(x_test)
# accuracy = np.mean(predicted == y_test)
# print(accuracy)
#
print("Running SVM classifier..")

text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                           alpha=1e-3, n_iter=5, random_state=42)),
                     ])
text_clf = text_clf.fit(x_train, y_train)
predicted = text_clf.predict(x_test)
accuracy = np.mean(predicted == y_test)
print(accuracy)

print("SVM detailed results..\n")

print(metrics.classification_report(y_test, predicted))
print(metrics.confusion_matrix(y_test, predicted))

print("SVM tuning using grid search..\n")

# TODO research how to use cost here.
parameters = {'tfidf__use_idf': (True, False),
              'clf__alpha': (0.1, 1e-2, 1e-3),
              }

gs_clf = GridSearchCV(text_clf, parameters, n_jobs=3)

gs_clf = gs_clf.fit(x_cv, y_cv)

best_parameters, score, _ = max(gs_clf.grid_scores_, key=lambda x: x[1])
for param_name in sorted(parameters.keys()):
    print("%s: %r" % (param_name, best_parameters[param_name]))

print(score)
