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

print("Retreived stock list...")

# Loop thru stock list
for stock in stock_codes['company_id']:

    print("Processing for.. " + str(stock))

    # Load all announcements for this stock.
    sql = "Select * from company_announcements where raw <> '' and " \
          "company_id = " + str(stock) + \
          " order by published_at DESC"
    temp = database.get_query_df(sql)
    announcements = Announcements(temp)

    print("Just queried DB.")

    # Load the test data for the announcements for this stock.
    df = announcements.get_test_data()

    print(df)

    data += df[0]
    labels += df[1]

    print("Calculated test data.")

print(data[:10])
print(labels[:10])

# Splitting the data up into 60% training set, 20% cross-validation and 20% testing sets.
x_train, x_cv_test, y_train, y_cv_test = cv.train_test_split(data, labels, test_size=0.40, random_state=1)
x_cv, x_test, y_cv, y_test = cv.train_test_split(x_cv_test, y_cv_test, test_size=0.50, random_state=1)

count_vect = CountVectorizer()
x_train_counts = count_vect.fit_transform(x_train)
x_train_counts.shape

count_vect.vocabulary_.get(u'algorithm')

tf_transformer = TfidfTransformer(use_idf=False).fit(x_train_counts)
x_train_tf = tf_transformer.transform(x_train_counts)
x_train_tf.shape

tfidf_transformer = TfidfTransformer()
x_train_tfidf = tfidf_transformer.fit_transform(x_train_counts)
x_train_tfidf.shape

clf = MultinomialNB().fit(x_train_tfidf, y_train)

# Testing the model on the test set.
x_test_counts = count_vect.transform(x_test)
x_test_tfidf = tfidf_transformer.transform(x_test_counts)

predicted = clf.predict(x_test_tfidf)

print(metrics.classification_report(y_test, predicted))

print(metrics.confusion_matrix(y_test, predicted))

#
# text_clf = Pipeline([('vect', CountVectorizer()),
#                      ('tfidf', TfidfTransformer()),
#                      ('clf', MultinomialNB()),
#                      ])
#
#
# twenty_test = fetch_20newsgroups(subset='test',
#                                  categories=categories, shuffle=True, random_state=42)
# docs_test = twenty_test.data
# predicted = text_clf.predict(docs_test)
# np.mean(predicted == twenty_test.target)
#
#
#
# text_clf = Pipeline([('vect', CountVectorizer()),
#                      ('tfidf', TfidfTransformer()),
#                      ('clf', SGDClassifier(loss='hinge', penalty='l2',
#                                            alpha=1e-3, n_iter=5, random_state=42)),
#                      ])
# _ = text_clf.fit(twenty_train.data, twenty_train.target)
# predicted = text_clf.predict(docs_test)
# np.mean(predicted == twenty_test.target)
#
#
# print(metrics.classification_report(twenty_test.target, predicted,
#                                     target_names=twenty_test.target_names))
#
#
# metrics.confusion_matrix(twenty_test.target, predicted)
#
#
# parameters = {'vect__ngram_range': [(1, 1), (1, 2)],
#               'tfidf__use_idf': (True, False),
#               'clf__alpha': (1e-2, 1e-3),
#               }
#
# gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)
#
# gs_clf = gs_clf.fit(twenty_train.data[:400], twenty_train.target[:400])
#
# twenty_train.target_names[gs_clf.predict(['God is love'])]
#
# best_parameters, score, _ = max(gs_clf.grid_scores_, key=lambda x: x[1])
# for param_name in sorted(parameters.keys()):
#     print("%s: %r" % (param_name, best_parameters[param_name]))
#
# score