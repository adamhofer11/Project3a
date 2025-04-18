# app.py
from flask import Flask, render_template, request
import csv
import traceback
from key import key
from main import get_symbol, render_chart

app = Flask(__name__)

#Load stock symbols from CSV
def load_symbols():
    symbols = []
    with open('stocks.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            symbols.append(row['Symbol'])
    return symbols

STOCK_SYMBOLS = load_symbols()

@app.route('/', methods=['GET', 'POST'])
def index():
    chart_created = False
    chart_filename = None
    symbol = None
    frame = None

    if request.method == 'POST':
        print("POST request received")
        try:
            symbol = request.form['symbol']
            print("Symbol:", symbol)

            chart_type = int(request.form['chart_type'])
            print("Chart Type:", chart_type)

            time_series = int(request.form['time_series'])
            print("Time Series:", time_series)

            frame = request.form.get('frame')
            print("Frame (raw):", frame)

            opens, highs, lows, closes, frame = get_symbol(symbol, time_series)
            print("get_symbol returned data")

            chart_filename = render_chart(chart_type, opens, highs, lows, closes)
            print("Chart rendered:", chart_filename)

            chart_created = True

        except Exception as e:
            print("ERROR OCCURRED:", e)
            traceback.print_exc()

    return render_template(
        'index.html',
        chart_created=chart_created,
        chart_filename=chart_filename,
        symbol=symbol,
        frame=frame,
        symbols=STOCK_SYMBOLS
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
