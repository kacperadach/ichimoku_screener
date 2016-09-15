from GetStockData import get_stock_data
from CalculateIchimoku import calculate_ichimoku

def get_stock_ichimoku(ticker, start_date, end_date):
    data = get_stock_data(ticker, start_date, end_date)
    if not data:
        return None
    today_ichimoku = calculate_ichimoku(ticker, data)
    yesterday_ichimoku = calculate_ichimoku(ticker, data[1:])
    today_cloud = calculate_ichimoku(ticker, data[25:])
    yesterday_cloud = calculate_ichimoku(ticker, data[26:])
    return {
        'today': today_ichimoku,
        'yesterday': yesterday_ichimoku,
        'today_cloud': today_cloud,
        'yesterday_cloud': yesterday_cloud,
        'today_data': data[0],
        'yesterday_data': data[1]
    }