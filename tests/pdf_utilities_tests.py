from pdf_utilities import *
from unittest.mock import patch
from urllib import parse, request
import os


def test_get_raw_text_from_fs_link():
    """Testing the raw text from pdf link getter"""
    directory = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(directory, "../resources/test_content_extract.pdf")
    fn_required_result = "b'one two three\\nfour five\\nsix\\n\\nseven\\n\\neight\\n\\nnine\\n\\n\\x0c'"
    fn_return = get_raw_text_from_fs_link(filename)
    assert fn_required_result == fn_return
