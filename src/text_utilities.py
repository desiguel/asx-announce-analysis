import re
import os
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import numpy as np

# Make stop word list available.
directory = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(directory, "../resources/stopwords/english")
stop = [line.strip() for line in open(filename, 'r')]


def clean_text(raw):
    """
    Clean text.
    :param raw: text string to be cleaned.
    :return:
    """
    raw = raw.lower()
    text = raw.replace('\\n', ' ')
    text = text.replace('for personal use only', ' ')
    text = re.sub('[0-9]', ' ', text)
    text = re.sub('[\W]+', ' ', text)
    text = re.sub('(\\b[A-Za-z]{1,2}\\b)', ' ', text)
    text = " ".join(text.split())

    return text


def remove_stop_words(text):
    """
    Removes the stop words in a string.
    :param text: string
    :return: string with stop words removed
    """
    stop = stopwords.words('english')
    new_list = [word for word in text.split() if word not in stop]
    return ' '.join(new_list)


def tokenised(text):
    """
    Return a tokenised text list.
    :param text: text string to be tokenised.
    :return: list
    """
    return [word for word in text.split()]


def stem_list(word_list):
    """
    Return a tokenised text list.
    :param word_list: word list to be stemmed.
    :return: list
    """
    stemmer = PorterStemmer()
    return [stemmer.stem(word) for word in word_list]


def remove_repeats(word_list):
    """
    Remove repeated words in a list.
    :param word_list:
    :return: list
    """
    seen = set()
    result = []
    for item in word_list:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def feature_reduction(data, labels, level):
    """
    Feature reduce a text data-set with three classes.
    :param data: a tf-idf dataset
    :param labels: data-set labels
    :param level: the % cutoff
    :return: reduced data-set
    """
    # Run 1 and 2 against the other one
    temp_labels = np.array([-1 if (v == 1 or v == 2) else 1 for i, v in enumerate(labels)])

    # Multiply through data
    data_a = np.absolute(data.transpose().dot(temp_labels))
    data_a_index = [i for i, v in enumerate(data_a) if v > level]

    # Run 1 and 0 against the other one
    temp_labels = np.array([-1 if (v == 1 or v == 0) else 1 for i, v in enumerate(labels)])

    # Multiply through data
    data_b = np.absolute(data.transpose().dot(temp_labels))
    data_b_index = [i for i, v in enumerate(data_b) if v > level]

    # Run 2 and 0 against the other one
    temp_labels = np.array([-1 if (v == 0 or v == 2) else 1 for i, v in enumerate(labels)])

    # Multiply through data
    data_c = np.absolute(data.transpose().dot(temp_labels))
    data_c_index = [i for i, v in enumerate(data_c) if v > level]

    # Convert these separate lists to a set, then back to a list
    results_list = [data_a_index, data_b_index, data_c_index]
    data_index = list(set().union(*results_list))

    data = data[:, data_index]

    return data
