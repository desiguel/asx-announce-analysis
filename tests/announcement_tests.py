import datetime
from announcement import *


def test_announcement_constructor():
    """Testing the announcement constructor."""
    announcement = Announcement(1045, datetime.datetime(2010, 10, 8, 0, 0), 1,
                               'Network expansion in South East Queensland', '01106368')
    assert isinstance(announcement, Announcement)


# TODO How to test functions which obtain external data?
# TODO Testing of private methods?

def test_announcement_get_text_list():
    """Testing the announcement get text list function."""
    announcement = Announcement(1045, datetime.datetime(2010, 10, 8, 0, 0), 1,
                                'Network expansion in South East Queensland', '01106368')
    announcement_text = announcement.get_text_list()
    # TODO
    assert False


def test_announcement_get_price_result():
    """Testing the announcement get_price_result function."""
    # TODO
    assert False


# TODO Assert stacking ok?

def test_announcement_is_sensitive():
    """Testing the announcement is_sensitive function."""
    announcement_true = Announcement(1045, datetime.datetime(2010, 10, 8, 0, 0), 1,
                                'Network expansion in South East Queensland', '01106368')
    announcement_false = Announcement(1045, datetime.datetime(2010, 10, 8, 0, 0), 0,
                                     'Network expansion in South East Queensland', '01106368')
    assert announcement_true.is_sensitive() == True
    assert announcement_false.is_sensitive() == False
