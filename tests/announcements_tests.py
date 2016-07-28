import datetime
import pandas as pd
from pandas.util.testing import assert_frame_equal
from announcements import *
from announcement import *
from database_mysql import *
from nose import with_setup
import os
from unittest.mock import patch
from urllib import parse, request


directory = os.path.dirname(os.path.realpath(__file__))


def setup():
    """set up test fixtures"""


def teardown():
    """tear down test fixtures"""


def test_announcements_constructor():
    """Testing the announcement constructor."""
    sql = "Select * from company_announcements where company_id = 1045 " \
          "order by published_at DESC"
    database = DatabaseMySQL()
    announcements = Announcements(database.get_query_df(sql))
    assert isinstance(announcements, Announcements)


def test_get_announcements():
    """Testing the announcement constructor."""
    sql = "Select * from company_announcements where company_id = 1045 " \
          "order by published_at DESC"
    database = DatabaseMySQL()
    announcements = Announcements(database.get_query_df(sql))
    df = announcements.get_announcements()
    assert isinstance(df, pd.DataFrame)


def test_generate_test_data():
    """Testing the function output structure."""
    filename = os.path.join(directory, "../resources/testing/pre_sens_flag.csv")
    df = pd.read_csv(filename)
    announcements = Announcements(df)
    assert isinstance(announcements, Announcements)


def test_add_pre_sens_flag():
    """Testing the addition of pre price sensitive flag."""
    filename = os.path.join(directory, "../resources/testing/pre_sens_flag.csv")
    df = pd.read_csv(filename)
    df['published_at'] = pd.to_datetime(df['published_at'], format="%d/%m/%y")
    df2 = df.copy(deep=True)
    announcements = Announcements(df2)
    announcements.add_pre_sens_flag()
    assert_frame_equal(announcements.df, df)


# @patch.object(Announcement, 'get_text_list', 'get_text_list("file")')
def test_get_test_data():
    """Testing the addition of pre price sensitive flag."""

    # Build required function result
    fn_required_result_corpora = ['three', 'seven', 'eleven', 'ten', 'five six']
    fn_required_result_pre_sens = [0, 0, 0, 1, 2]

    # Build fn_input
    filename = os.path.join(directory, "../resources/testing/pre_sens_flag.csv")
    df = pd.read_csv(filename)
    df['published_at'] = pd.to_datetime(df['published_at'], format="%d/%m/%y")
    file_prefix = directory + "/../resources/testing/pdfs/"
    df['link'] = file_prefix + df['link']
    df2 = df.copy(deep=True)

    announcements = Announcements(df2)
    fn_return_corpora, fn_return_pre_sens = announcements.get_test_data("file")

    print(fn_required_result_corpora)
    print(fn_return_corpora)
    print(fn_required_result_pre_sens)
    print(fn_return_pre_sens)

    assert fn_required_result_corpora == fn_return_corpora
    assert fn_required_result_pre_sens == fn_return_pre_sens

