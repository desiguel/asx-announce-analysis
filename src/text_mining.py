from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn import cross_validation as cv
from sklearn import metrics
from time import time
import pickle
import warnings
from text_utilities import *

# Ignore deprecation warnings.
warnings.filterwarnings("ignore")

# Script Precondition:
# Need to have data.pkl and labels.pkl available.
# Run load_data.py to generate these files if haven't already done so.

# Load data.
data = pickle.load(open('data_all.pkl', "rb"))
labels = pickle.load(open('labels_all.pkl', "rb"))

# Transform the data - vectorise and apply tf-idf.
data = CountVectorizer().fit_transform(data)
tf_idf_transform = TfidfTransformer(use_idf=True).fit(data)
data = tf_idf_transform.transform(data)

print("\nData frame shape:")
print(data.shape)

# Dimensionality reduction
print("\nRunning dimensionality reduction (custom)")
data = feature_reduction(data, labels, 0.80)

print("\nData frame shape after dimensionality reduction (custom):")
print(data.shape)

# Splitting the data up into 60% training set, 20% cross-validation and 20% testing sets.
x_train, x_cv_test, y_train, y_cv_test = cv.train_test_split(data, labels, test_size=0.40, random_state=1)
x_cv, x_test, y_cv, y_test = cv.train_test_split(x_cv_test, y_cv_test, test_size=0.50, random_state=1)

# # Test NB classifier
# print("\nRunning Naive Bayes classifier..")
# t0 = time()
#
# classifier_nb = MultinomialNB().fit(x_train, y_train)
# predicted = classifier_nb.predict(x_test)
# accuracy = np.mean(predicted == y_test)
#
# print("\nNaive Bayes model accuracy is: %0.2f" % accuracy)
#
# print(metrics.classification_report(y_test, predicted))
# print(metrics.confusion_matrix(y_test, predicted))
#
# t1 = time()
# print("\nNB classification time: {} sec".format(round((t1-t0), 2)))

# Test Logistical Regression classifier
print("\nRunning Logistic Regression classifier and tuning using grid search..")
t0 = time()

# Grid search for best LR parameters
cost_range = [1e-3, 0.1, 1, 100]
parameters = dict(C=cost_range)
grid = GridSearchCV(LogisticRegression(), param_grid=parameters, cv=None, n_jobs=7, verbose=3)
grid.fit(x_train, y_train)

print("\nThe best LR parameters are %s with a score of %0.2f"
      % (grid.best_params_, grid.best_score_))

predicted = grid.predict(x_test)
accuracy = np.mean(predicted == y_test)

print(metrics.classification_report(y_test, predicted))
print(metrics.confusion_matrix(y_test, predicted))

t1 = time()
print("\nLR classification time: {} sec".format(round((t1-t0), 2)))

print("\nRunning SVM classifier and tuning using grid search..\n")
t0 = time()

# Grid search for best SVM parameters
cost_range = [1e-3, 0.1, 1, 10, 100, 1000]
gamma_range = [1e-9, 1e-5, 0.1, 1, 10, 100]
parameters = dict(gamma=gamma_range, C=cost_range)
grid = GridSearchCV(SVC(), param_grid=parameters, cv=None, n_jobs=7, verbose=3)
grid.fit(x_train, y_train)

print("\nThe best SVM parameters are %s with a score of %0.2f"
      % (grid.best_params_, grid.best_score_))
print("\nClassification time: {} sec".format(round((t1-t0), 2)))

predicted = grid.predict(x_test)
accuracy = np.mean(predicted == y_test)

print(metrics.classification_report(y_test, predicted))
print(metrics.confusion_matrix(y_test, predicted))

t1 = time()
print("\nSVM classification time: {} sec".format(round((t1-t0), 2)))

print("\nRunning MLP classifier and tuning using grid search..\n")
t0 = time()

# Grid search for best SVM parameters
alpha_range = [1e-5, 1e-3, 0.1, 10, 100]
layer1_range = [5, 10, 30, 40, 50]
layer2_range = [5, 10, 30, 40, 50]
layer3_range = [5, 10, 30, 40, 50]
parameters = dict(solver=['lbfgs'], alpha=alpha_range,
                  hidden_layer_sizes=(layer1_range, layer2_range, layer3_range), random_state=[1])
grid = GridSearchCV(MLPClassifier(), param_grid=parameters, cv=None, n_jobs=7, verbose=3)
grid.fit(x_train, y_train)

print("\nThe best MLP parameters are %s with a score of %0.2f"
      % (grid.best_params_, grid.best_score_))
print("\nClassification time: {} sec".format(round((t1-t0), 2)))

predicted = grid.predict(x_test)
accuracy = np.mean(predicted == y_test)

print(metrics.classification_report(y_test, predicted))
print(metrics.confusion_matrix(y_test, predicted))

t1 = time()
print("\nMLP classification time: {} sec".format(round((t1-t0), 2)))