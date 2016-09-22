from pdf_utilities import *
import pandas as pd
from unittest.mock import patch
from urllib import parse, request
from nose import with_setup
import os


def setup():
    """set up test fixtures"""
    directory = os.path.dirname(os.path.realpath(__file__))


def teardown():
    """tear down test fixtures"""


@with_setup(setup, teardown)
def test_get_raw_text_from_fs_link():
    """Testing the raw text from pdf link getter"""
    filename = os.path.join(directory, "../resources/testing/pdfs/content_extract.pdf")
    fn_required_result = "b'one two three\\nfour five\\nsix\\n\\nseven\\n\\neight\\n\\nnine\\n\\n\\x0c'"
    fn_return = get_raw_text_from_fs_link(filename)
    assert fn_required_result == fn_return


@with_setup(setup, teardown)
def test_add_pre_sens_flag():
    filename = os.path.join(directory, "../resources/testing/pre_sens_flag.csv")
    df = pd.read_csv(filename)
