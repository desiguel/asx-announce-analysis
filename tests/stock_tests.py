from stock import *
import pandas as pd

def test_stock_constructor():
    """
    Testing the announcement constructor.
    """
    stock = Stock(1045)
    assert isinstance(stock, Stock)

def test_get_asx_code():
    """
    Testing the get_asx_code function
    """
    stock = Stock(1045)
    fn_required_result = "ONT.ASX"
    fn_return = stock.get_asx_code()
    assert fn_return == fn_required_result

def test_get_price_history():
    """
    Testing the retrieval of price history for a stock.
    Only tests for return of a dataframe.
    """
    stock = Stock(1045)
    fn_return = stock.get_price_history()
    assert isinstance(fn_return, pd.DataFrame)
