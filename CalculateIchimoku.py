from ichimoku import ichimoku

def calculate_ichimoku(ticker, data):
    conversion_line = _calculate_lines(data[0:9])
    base_line = _calculate_lines(data[0:26])
    span_a = _calculate_span_a(conversion_line, base_line)
    span_b = _calculate_lines(data[0:52])
    if all(x is not None for x in (conversion_line, base_line, span_a, span_b)):
        return ichimoku(ticker, conversion_line, base_line, span_a, span_b)


def _calculate_lines(data):
    try:
        high, low = None, None
        for d in data:
            if high is None:
                high = float(d['High'])
            if low is None:
                low = float(d['Low'])
            high = float(d['High']) if float(d['High']) > high else high
            low = float(d['Low']) if float(d['Low']) < low else low
        line = (low + high) / 2
        return line
    except:
        return

def _calculate_span_a(conversion_line, base_line):
    if conversion_line is not None and base_line is not None:
        return (conversion_line + base_line) /2


