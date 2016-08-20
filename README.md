# Ichimoku Screener

This code is a daily stock screener I wrote that goes through all NYSE, NASDAQ and AMEX stocks and calculates their ichimoku values to determine if an important price event has occured. It gathers the stock tickers and automatically sends an email to everyone on the [email list.](https://docs.google.com/spreadsheets/d/1yJkEd5u12niaFBPlglZO63iM4nSf-SYaXaBFhVCWX8Q/edit#gid=0)

### What is Ichimoku?

The Ichimoku Cloud is a technical indicator used most commonly on financial securities to better understand current and future price action. The cloud is particularly useful because it has two leading spans that are plotted 26 periods ahead on the chart. These spans give an indication of the future trend prices may take, which when combined with other technical analysis tools, can be used to trade more profitably.

[StockCharts explanation](http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ichimoku_cloud)

### What does this screener look for?

My screener (which is still a work in progress) looks for Tenkan-sen/Kijun-sen (TK) crosses, bullish cloud folds (span A overtakes span B) and price action that leaves the cloud in a bullish manner. It filters stocks based on volume, marketcap and PE ratio, as well as stocks under $1.00 (no pennystocks).

### How do I get on the email list?

Add your name in the A column of the [Google Sheet.](https://docs.google.com/spreadsheets/d/1yJkEd5u12niaFBPlglZO63iM4nSf-SYaXaBFhVCWX8Q/edit#gid=0)

### When do I get the email?

Sometime between 9-10pm EST. The screener takes about an hour to run and I try to wait a couple hours after market close so that yahoo finance can give me up to date historical data. Also, it is still a work in progress so occasionally errors stop it from running and I have to execute it manually.

### Trading Advice

The stocks sent in the email are NOT a buying recommendation. They are simply stocks that could be at a pivotal point in their price action. If you don't understand Ichimoku Cloud or stock charts in general this screener will not be very helpful.
