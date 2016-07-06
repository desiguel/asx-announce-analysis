from text_utilities import *


def test_clean_text():
    """Testing the clean_text function."""
    fn_input = "Four \\n 23,%^ an"
    fn_required_result = "four"
    fn_return = clean_text(fn_input)
    assert fn_return == fn_required_result


def test_remove_stop_words():
    """Testing the remove_stop_words function."""
    fn_input = "four and five to six an"
    fn_required_result = 'four five six'
    fn_return = remove_stop_words(fn_input)
    assert fn_return == fn_required_result


def test_tokenised():
    """Testing the tokenised function."""
    fn_input = "four five"
    fn_required_result = ['four', 'five']
    fn_return = tokenised(fn_input)
    assert fn_return == fn_required_result


def test_stem_list():
    """Testing the stem_list function."""
    fn_input = ['teaming', 'team', 'reduced', 'reduce']
    fn_required_result = ['team', 'team', 'reduc', 'reduc']
    fn_return = stem_list(fn_input)
    assert fn_return == fn_required_result


def test_remove_repeats():
    """Testing the remove_repeats function."""
    fn_input = ['team', 'team', 'reduc', 'reduc', 'new', 'a']
    fn_required_result = ['team', 'reduc', 'new', 'a']
    fn_return = remove_repeats(fn_input)
    assert fn_return == fn_required_result
