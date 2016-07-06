from nose import with_setup  # optional
from text_utilities import *


def setup_module(module):
    print("")  # this is to get a newline after the dots
    print("setup_module before anything in this file")


def teardown_module(module):
    print("teardown_module after everything in this file")


def my_setup_function():
    print("my_setup_function")


def my_teardown_function():
    print("my_teardown_function")


def test_clean_text():
    print('Testing the clean_text function.')
    fn_input = "Four \\n 23,%^ an"
    fn_required_result = "four"
    fn_return = clean_text(fn_input)
    assert fn_return == fn_required_result

def test_remove_stop_words():
    print('Testing the removal of stop words from a string function.')
    fn_input = "four and five to six an"
    fn_required_result = 'four five six'
    fn_return = remove_stop_words(fn_input)
    assert fn_return == fn_required_result

def test_tokenised():
    print('Testing the tokenised function.')
    fn_input = "four five"
    fn_required_result = ['four', 'five']
    fn_return = tokenised(fn_input)
    assert fn_return == fn_required_result

def test_stem_list():
    print('Testing the stemming of a list of words.')
    fn_input = ['teaming', 'team', 'reduced', 'reduce']
    fn_required_result = ['team', 'team', 'reduc', 'reduc']
    fn_return = stem_list(fn_input)
    assert fn_return == fn_required_result

def test_remove_repeats():
    print('Testing the removal of repeated words from a list.')
    fn_input = ['team', 'team', 'reduc', 'reduc', 'new', 'a']
    fn_required_result = ['team', 'reduc', 'new', 'a']
    fn_return = remove_repeats(fn_input)
    assert fn_return == fn_required_result