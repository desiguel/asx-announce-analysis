import datetime
import pandas as pd
from announcements import *
from database import *


def test_announcements_constructor():
    """Testing the announcement constructor."""
    sql = "Select * from company_announcements where company_id = 1045 " \
          "order by published_at DESC"
    database = Database()
    announcements = Announcements(database.get_query_result(sql))
    assert isinstance(announcements, Announcements)


def test_get_announcements():
    """Testing the announcement constructor."""
    sql = "Select * from company_announcements where company_id = 1045 " \
          "order by published_at DESC"
    database = Database()
    announcements = Announcements(database.get_query_result(sql))
    df = announcements.get_announcements()
    assert isinstance(df, pd.DataFrame)


def test___generate_test_data():
    """Testing the function output structure."""
    # TODO
    assert False