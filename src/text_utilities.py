import re
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords


def clean_text(raw):
    """
    Clean text.
    :param raw: text string to be cleaned.
    :return:
    """
    raw = raw.lower()
    text = raw.replace('\\n', ' ')
    text = re.sub('[0-9]', ' ', text)
    text = re.sub('[\W]+', ' ', text)
    text = re.sub('(\\b[A-Za-z]{1,2}\\b)', ' ', text)
    text = text.strip()

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
