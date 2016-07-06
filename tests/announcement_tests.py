from nose import with_setup  # optional
import datetime
from announcement import *


def setup_module(module):
    print("")  # this is to get a newline after the dots
    print("setup_module before anything in this file")


def teardown_module(module):
    print("teardown_module after everything in this file")


def my_setup_function():
    print("my_setup_function")


def my_teardown_function():
    print("my_teardown_function")


def test_announcement_constructor():
    print('Testing the announcement constructor.')
    announcement = Announcement(1045, datetime.datetime(2010, 10, 8, 0, 0), 1,
                               'Network expansion in South East Queensland', '01106368')
    assert isinstance(announcement, Announcement)


# TODO How to test functions which obtain external data?
# TODO Testing of private methods?

def test_announcement_get_text_list():
    print('Testing the announcement get text list function.')
    announcement = Announcement(1045, datetime.datetime(2010, 10, 8, 0, 0), 1,
                                'Network expansion in South East Queensland', '01106368')
    assert False

def test_announcement_get_price_result():
    print('Testing the announcement get_price_result function.')
    assert False

# TODO Assert stacking ok?

def test_announcement_is_sensitive():
    print('Testing the announcement is_sensitive function.')
    announcement_true = Announcement(1045, datetime.datetime(2010, 10, 8, 0, 0), 1,
                                'Network expansion in South East Queensland', '01106368')
    announcement_false = Announcement(1045, datetime.datetime(2010, 10, 8, 0, 0), 0,
                                     'Network expansion in South East Queensland', '01106368')
    assert announcement_true.is_sensitive() == True
    assert announcement_false.is_sensitive() == False
