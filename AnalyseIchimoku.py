from GetStockTickers import get_all_tickers_from_ftp
from GetStockIchimoku import get_stock_ichimoku
from Logger import get_logger

logger = get_logger()

def analyze_ichimoku():
    cross_above, cross_inside, cross_below, price_leaving_cloud, cloud_fold = ([] for i in range(5))
    tickers = get_all_tickers_from_ftp()
    for t in tickers:
        logger.info("Analyzing ticker: {}".format(t))
        ichimoku_data = get_stock_ichimoku(t)
        if not ichimoku_data:
            continue
        cross_above, cross_inside, cross_below, price_leaving_cloud, cloud_fold = classify_ichimoku(ichimoku_data, cross_above, cross_inside, cross_below, price_leaving_cloud, cloud_fold)
    overlap = set(cloud_fold).intersection(cross_above + cross_inside + cross_below)
    return {
        'cross_above': [x for x in cross_above if x not in overlap],
        'cross_inside': [x for x in cross_inside if x not in overlap],
        'cross_below': [x for x in cross_below if x not in overlap],
        'price_leaving_cloud': [x for x in price_leaving_cloud if x not in overlap],
        'cloud_fold': [x for x in cloud_fold if x not in overlap],
        'overlap': overlap
    }

def classify_ichimoku(ichimoku_data, cross_above, cross_inside, cross_below, price_leaving_cloud, cloud_fold):
    today_cloud, yesterday_cloud = ichimoku_data['today_cloud'], ichimoku_data['yesterday_cloud']
    today_data, yesterday_data = ichimoku_data['today_data'], ichimoku_data['yesterday_data']
    today_ichi, yesterday_ichi = ichimoku_data['today'], ichimoku_data['yesterday']
    if (yesterday_ichi.conversion_line <= yesterday_ichi.base_line and today_ichi.conversion_line > today_ichi.base_line) or \
            (yesterday_ichi.conversion_line < yesterday_ichi.base_line and today_ichi.conversion_line >= today_ichi.base_line):
        if today_ichi.base_line == today_ichi.conversion_line:
            intersection = today_ichi.base_line
        else:
            intersection = get_intersection_point(yesterday_ichi.conversion_line, today_ichi.conversion_line, yesterday_ichi.base_line, today_ichi.base_line)
        if below(intersection, today_cloud):
            cross_below.append(today_ichi.ticker)
        elif inside(intersection, today_cloud):
            cross_inside.append(today_ichi.ticker)
        elif above(intersection, today_cloud):
            cross_above.append(today_ichi.ticker)
        else:
            logger.info("TK cross found but not classified for {}".format(today_ichi.ticker))
    if price_action_leaving_cloud(today_cloud, yesterday_cloud, today_data, yesterday_data) and today_cloud.is_cloud_green():
        price_leaving_cloud.append(today_ichi.ticker)
    if yesterday_ichi.leading_span_a <= yesterday_ichi.leading_span_b and today_ichi.leading_span_a > today_ichi.leading_span_b or yesterday_ichi.leading_span_a < yesterday_ichi.leading_span_b and today_ichi.leading_span_a >= today_ichi.leading_span_b:
        if today_ichi.conversion_line > today_ichi.base_line:
            cloud_fold.append(today_ichi.ticker)
    return cross_above, cross_inside, cross_below, price_leaving_cloud, cloud_fold

def price_action_leaving_cloud(today_cloud, yesterday_cloud, today_data, yesterday_data):
    if inside_range([yesterday_data['High'], yesterday_data['Low']], [yesterday_cloud.leading_span_a, yesterday_cloud.leading_span_b]):
        if today_cloud.is_cloud_green():
            comparison = today_cloud.leading_span_a
        else:
            return False
        if float(today_data['Close']) > comparison:
            return True
    return False

def below(intersection, today_cloud):
    return intersection < today_cloud.leading_span_a and intersection < today_cloud.leading_span_b

def inside(intersection, today_cloud):
    return in_float_range(intersection, today_cloud.leading_span_b, today_cloud.leading_span_a)


def in_float_range(num, range_a, range_b):
    if range_a > range_b:
        return num >= range_b and num <= range_a
    else:
        return num <= range_b and num >= range_a

def above(intersection, today_cloud):
    return intersection > today_cloud.leading_span_a and intersection > today_cloud.leading_span_b


def get_intersection_point(a, b, x, y):
    conversion = get_line_equation([0, a], [1, b])
    base = get_line_equation([0, x], [1, y])
    x_intersection = (base[1] - conversion[1]) / (conversion[0] - base[0])
    y_intersection = (base[0] * x_intersection) + base[1]
    return y_intersection

def get_line_equation(p1, p2):
    slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
    intercept = (-1 * slope * p1[0]) + p1[1]
    return slope, intercept


def inside_range(data, range):
    return float(min(data)) > float(min(range)) and float(max(data)) < float(max(range))
