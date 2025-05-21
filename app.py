from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

from datetime import datetime, timedelta
import pandas as pd

def resolve_symbol(ticker: str) -> str:
    df = okama.symbols_in_namespace('US')
    match = df[df['ticker'].str.upper() == ticker.upper()]
    if not match.empty:
        return match.iloc[0]['symbol']
    raise ValueError(f"Тикер {ticker} не найден в namespace 'US'")

def get_asset_prices(user_input_ticker):
    symbol = resolve_symbol(user_input_ticker)
    asset = okama.Asset(symbol)
    prices = asset.close_daily

    # Преобразуем индекс к datetime
    prices.index = prices.index.to_timestamp()

    # Фильтруем за последние 6 месяцев
    six_months_ago = datetime.today() - timedelta(days=180)
    return prices[prices.index >= six_months_ago]



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/correlate')
def correlate():
    ticker1 = request.args.get('ticker1')
    ticker2 = request.args.get('ticker2')

    if not ticker1 or not ticker2:
        return jsonify({"error": "Оба тикера обязательны"}), 400

    try:
        s1 = get_asset_prices(ticker1)
        s2 = get_asset_prices(ticker2)
        df = pd.concat([s1.rename('A'), s2.rename('B')], axis=1).dropna()
        if df.empty:
            return jsonify({"error": "Недостаточно данных для анализа"}), 400
        corr = df.corr().iloc[0, 1]
        return jsonify({"correlation": round(corr, 4)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/prices')
def get_prices():
    ticker1 = request.args.get('ticker1')
    ticker2 = request.args.get('ticker2')

    try:
        s1 = get_asset_prices(ticker1)
        s2 = get_asset_prices(ticker2)
        df = pd.concat([s1.rename('A'), s2.rename('B')], axis=1).dropna()
        df.index = df.index.strftime('%Y-%m-%d')  # форматируем даты как строки
        return jsonify({
            "labels": df.index.tolist(),
            "series1": df['A'].tolist(),
            "series2": df['B'].tolist()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    import okama

    us_assets = okama.symbols_in_namespace('US')  # ✅
    print(us_assets[:10])  # первые 10 тикеров
    assets = okama.symbols_in_namespace('US')
    print(assets['type'].value_counts())
    df = okama.symbols_in_namespace('US')

    # Фильтруем по тикеру (всё в верхнем регистре)
    filtered = df[df['ticker'].str.upper() == 'KO']
    print(filtered)

    app.run(debug=True)
