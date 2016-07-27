#!/usr/bin/python3

from database import Database

def __get_price_near(stock, datetime, greater_or_less_than):
    """Get the price immediately before or after a datetime that shows
    positive volume."""
    datetime_for_sql = datetime.strftime("%Y-%m-%d")
    database = Database()
    sql = "Select `last` from company_price_history where \
           company_id = " + str(stock) + " and \
           published_at " + greater_or_less_than + \
          " STR_TO_DATE('" + datetime_for_sql + "','%Y-%m-%d') \
           and volume > 0 order by published_at DESC LIMIT 1"
    price = database.get_query_result(sql).iloc[0, 0]

    return price


def get_price_before(stock, datetime):
    """Get the price recorded on the next day before the datetime that shows
    positive volume."""
    return __get_price_near(stock, datetime, "<")


def get_price_after(stock, datetime):
    """Get the price recorded on the next day after the datetime that shows
    positive volume."""
    return __get_price_near(stock, datetime, ">")


def get_price_sign(stock, datetime):
    """Get the sign of the price move from before to after an event."""
    price_before = get_price_before(stock, datetime)
    price_after = get_price_after(stock, datetime)
    price_diff = price_after - price_before

    if price_diff < 0:
        return 0
    return 1
