from database import *
import pandas as pd

def test_database_constructor():
    """Testing the announcement constructor."""
    database = Database()
    assert isinstance(database, Database)

def test_get_query_result():
    """Testing database querying"""
    database = Database()
    fn_result = database.get_query_result("select 1")
    assert isinstance(fn_result, pd.DataFrame)
    assert fn_result.iloc[0, 0] == 1
