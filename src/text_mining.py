from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import PCA, IncrementalPCA
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
data = feature_reduction(data, labels, 0.85)

print("\nData frame shape after dimensionality reduction (custom):")
print(data.shape)

# Dimensionality reduction
print("\nRunning dimensionality reduction (PCA)")
pca = IncrementalPCA(n_components=50, batch_size=100)
pca.fit(data.toarray())
data = pca.transform(data.toarray())

print("\nPCA explained variance:")
print(pca.explained_variance_ratio_)
print(sum(pca.explained_variance_ratio_))

print("\nData frame shape after dimensionality reduction (custom):")
print(data.shape)

# Splitting the data up into 60% training set, 20% cross-validation and 20% testing sets.
x_train, x_test, y_train, y_test = cv.train_test_split(data, labels, test_size=0.30, random_state=1)

# Test Logistical Regression classifier
print("\nRunning Logistic Regression classifier and tuning using grid search..")
t0 = time()

# Grid search for best LR parameters
cost_range = [1e-3, 0.1, 1, 100]
parameters = dict(C=cost_range)
grid = GridSearchCV(LogisticRegression(), param_grid=parameters, cv=2, n_jobs=7, verbose=3)
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
cost_range = [0.1, 1, 10, 100, 1000]
gamma_range = [1e-5, 0.1, 1, 10, 100]
parameters = dict(gamma=gamma_range, C=cost_range)
grid = GridSearchCV(SVC(), param_grid=parameters, cv=2, n_jobs=7, verbose=3)
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
hidden_layer_range = np.vstack(np.meshgrid(layer1_range, layer2_range, layer3_range)).reshape(3, -1).T
hidden_layer_range = [tuple(i) for i in hidden_layer_range]

parameters = dict(solver=['lbfgs'], alpha=alpha_range,
                  hidden_layer_sizes=hidden_layer_range, random_state=[1])
grid = GridSearchCV(MLPClassifier(), param_grid=parameters, cv=2, n_jobs=7, verbose=3)
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