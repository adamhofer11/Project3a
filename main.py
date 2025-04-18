import requests
import pygal
import lxml

import key

def main():
    print("Stock Data Visualizer\n----------------------------\n")

    symbol = input("Enter the stock symbol you are looking for: ")
    print("----------------------------")

    chart = input("Enter chart type: \n1. Line \n2. Bar\n")
    print("----------------------------")
    chart_type = validate_chart(chart)

    time_series = input("Enter time series: \n1. Intraday \n2. Daily \n3. Weekly \n4. Monthly\n")
    print("----------------------------")
    time = validate_time(time_series)

    opens, highs, lows, closes, frame = get_symbol(symbol, time)
    render_chart(chart_type, opens, highs, lows, closes)

def validate_chart(chart):
    while chart not in ['1', '2']:
        print("Invalid selection. Please enter a valid chart type.")
        chart = input("Enter chart type: \n1. Line \n2. Bar\n")
    return int(chart)

def validate_time(time):
    while time not in ['1', '2', '3', '4']:
        print("Invalid selection. Please enter a valid time series.")
        time = input("Enter time series: \n1. Intraday \n2. Daily \n3. Weekly \n4. Monthly\n")
    return int(time)

def get_symbol(symbol, time):
    series = None
    frame = None

    if time == 1:
        frame = "Time Series (5min)"
        series = "TIME_SERIES_INTRADAY"
    elif time == 2:
        frame = "Time Series (Daily)"
        series = "TIME_SERIES_DAILY"
    elif time == 3:
        frame = "Weekly Time Series"
        series = "TIME_SERIES_WEEKLY"
    elif time == 4:
        frame = "Monthly Time Series"
        series = "TIME_SERIES_MONTHLY"

    url = f'https://www.alphavantage.co/query?function={series}&symbol={symbol}&interval=5min&apikey={key.key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return filter_data(data, frame)
    else:
        return response.status_code

def filter_data(data, frame):
    if frame == None:
        print("Error Getting Frame")
        quit()

    time_series = data.get(f"{frame}", {})

    open_prices = []
    high_prices = []
    low_prices = []
    close_prices = []

    for timestamp, values in time_series.items():
        open_prices.append(float(values["1. open"]))
        high_prices.append(float(values["2. high"]))
        low_prices.append(float(values["3. low"]))
        close_prices.append(float(values["4. close"]))

    return open_prices, high_prices, low_prices, close_prices, frame


def render_chart(chart_type, opens, highs, lows, closes):
    import os
    from pygal import Line, Bar
    from pygal.style import Style

    custom_style = Style(
        background='white',
        plot_background='white',
        foreground='black',
        foreground_strong='black',
        foreground_subtle='grey',
        colors=('blue', 'green', 'red', 'orange')
    )


    if chart_type == 1:
        chart = Line(style=custom_style)
        chart.title = 'Stock Prices (Line Chart)'
        chart.add('Close', closes)
        filename = 'line_chart.svg'

    elif chart_type == 2:
        chart = Bar(style=custom_style, width=1200, height=600)
        chart.title = 'Stock Prices (Bar Chart)'
        chart.add('Open', opens)
        chart.add('High', highs)
        chart.add('Low', lows)
        chart.add('Close', closes)
        filename = 'bar_chart.svg'

    chart.render_to_file(os.path.join("static", filename))

    return filename


def line_chart(closes):
    line_chart = pygal.Line()
    line_chart.title = 'Stock Closing Prices Over Time'
    line_chart.add('Close', closes, fill_opacity=0.3)
    
    #embeds css file
    line_chart.render_to_file('line_chart.svg', css=['styles.css'])
    print("Line chart saved as 'line_chart.svg'")

def bar_chart(opens, highs, lows, closes):
    bar_chart = pygal.Bar()
    bar_chart.title = 'Stock Prices (Open, High, Low, Close)'
    bar_chart.add('Open', opens)
    bar_chart.add('High', highs)
    bar_chart.add('Low', lows)
    bar_chart.add('Close', closes)
    bar_chart.render_to_file('bar_chart.svg', css=['styles.css'])
    print("Bar chart saved as 'bar_chart.svg'")

if __name__ == "__main__":
    main()