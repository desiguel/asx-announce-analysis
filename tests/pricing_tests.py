from pricing import *
import datetime

def test_get_price_before():
    """Testing the get_price_after_event function."""
    fn_input_stock = "1045"
    fn_input_datetime = datetime.datetime(2015, 12, 21, 0, 0)
    fn_required_result = 7.5
    fn_return = get_price_before(fn_input_stock, fn_input_datetime)

    assert fn_return == fn_required_result


def test_get_price_after():
    """Testing the get_price_after_event function."""
    fn_input_stock = "1045"
    fn_input_datetime = datetime.datetime(2015, 12, 21, 0, 0)
    fn_required_result = 7.07
    fn_return = get_price_after(fn_input_stock, fn_input_datetime)

    assert fn_return == fn_required_result


def test_get_price_sign():
    """Testing the get_price_after_event function."""
    fn_input_stock = "1045"
    fn_input_datetime = datetime.datetime(2015, 12, 21, 0, 0)
    fn_required_result = 0
    fn_return = get_price_sign(fn_input_stock, fn_input_datetime)

    assert fn_return == fn_required_result
