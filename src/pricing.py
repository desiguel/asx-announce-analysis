#!/usr/bin/python3

from database_mysql import DatabaseMySQL

def __get_price_near(stock, datetime, greater_or_less_than):
    """Get the price immediately before or after a datetime that shows
    positive volume."""
    datetime_for_sql = datetime.strftime("%Y-%m-%d")
    database = DatabaseMySQL()

    order_by = ""
    if greater_or_less_than == "<":
        order_by = "DESC"

    sql = "Select close from company_price_volume_history where " + \
          "company_id = " + str(stock) + " and " + \
          "published_at " + greater_or_less_than + \
          " STR_TO_DATE('" + datetime_for_sql + "','%Y-%m-%d')" + \
          "and volume > 0 order by published_at " + order_by + " LIMIT 1"

    df = database.get_query_df(sql)

    # Default the return price to 0. Will only matter when a record is not returned.
    price = 0
    if not df.empty:
        price = df.iloc[0, 0]

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
