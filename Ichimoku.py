class ichimoku:

    def __init__(self, ticker, conversion_line, base_line, leading_span_a, leading_span_b):
        self.ticker = ticker
        self.conversion_line = conversion_line
        self.base_line = base_line
        self.leading_span_a = leading_span_a
        self.leading_span_b = leading_span_b

    def __repr__(self):
        conversion = "Conversion line: {}".format(self.conversion_line)
        base_line = "Base line: {}".format(self.base_line)
        span_a = "Span a: {}".format(self.leading_span_a)
        span_b = "Span b: {}".format(self.leading_span_b)
        return "\n".join([conversion, base_line, span_a, span_b])

    def is_cloud_green(self):
        return self.leading_span_a > self.leading_span_b
