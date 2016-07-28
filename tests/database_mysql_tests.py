from database_mysql import *
import pandas as pd


def test_database_constructor():
    """Testing the announcement constructor."""
    database = DatabaseMySQL()
    assert isinstance(database, DatabaseMySQL)


def test_get_query_result():
    """Testing database querying"""
    database = DatabaseMySQL()
    fn_result = database.get_query_df("select 1")
    assert isinstance(fn_result, pd.DataFrame)
    assert fn_result.iloc[0, 0] == 1
