from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from text_utilities import *


class ML(object):
    """
    Class setup for the application of machine learning techniques to data.
    """

    def __init__(self, x_train, y_train, x_test, y_test):
        """
        Return a ML (Machine Learning) object.
        """
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.gs_lr_tfidf = None

    def __process_text(raw):
        """Take some text, process it and return a list."""
        text = clean_text(raw)
        # text = remove_stop_words(text)
        word_list = tokenised(text)
        word_list = stem_list(word_list)
        return word_list


    def calculate_logistic_regression(self):
        """Logistic regression model, fit and test."""
        tfidf = TfidfVectorizer(strip_accents=None,
                                lowercase=False,
                                preprocessor=None)

        param_grid = [{'vect__ngram_range': [(1, 1)],
                       'vect__stop_words': [stop, None],
                       'vect__tokenizer': [self.__process_text],
                       'clf__penalty': ['l1', 'l2'],
                       'clf__C': [1.0, 10.0, 100.0]},
                      {'vect__ngram_range': [(1, 1)],
                       'vect__stop_words': [stop, None],
                       'vect__tokenizer': [self.__process_text],
                       'vect__use_idf':[False],
                       'vect__norm':[None],
                       'clf__penalty': ['l1', 'l2'],
                       'clf__C': [1.0, 10.0, 100.0]},
                      ]

        lr_tfidf = Pipeline([('vect', tfidf),
                             ('clf', LogisticRegression(random_state=0))])

        self.gs_lr_tfidf = GridSearchCV(lr_tfidf, param_grid,
                                   scoring='accuracy',
                                   cv=5,
                                   verbose=1,
                                   n_jobs=-1)

        self.gs_lr_tfidf.fit(self.x_train, self.y_train)

    def print_logistic_regression_result(self):
        """Print the results of the logistic regression analysis."""
        print('Best parameter set: %s ' % self.gs_lr_tfidf.best_params_)
        print('CV Accuracy: %.3f' % self.gs_lr_tfidf.best_score_)

        clf = self.gs_lr_tfidf.best_estimator_
        print('Test Accuracy: %.3f' % clf.score(self.x_test, self.y_test))