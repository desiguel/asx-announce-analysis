from pdf_utilities import *
from unittest.mock import patch
from urllib import parse, request
import os


# TODO How to setup a mock pdf that can be read in as a stream?
def test_get_raw_text_from_link():
    """Testing the raw text from pdf link getter"""
    fn_required_result = "one two three four five six seven eight nine"
    fn_return = get_raw_text_from_link(".\\resources\\test_content_extract.pdf")
    assert False

