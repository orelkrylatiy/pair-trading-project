# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # Чтобы фронт мог обращаться к API

app = Flask(__name__)
CORS(app)  # Разрешаем запросы со стороны фронта (другой порт)

@app.route('/')
def index():
    return "Welcome to the Stock Correlation API!"

@app.route('/api/correlation')
def correlation():
    ticker1 = request.args.get('ticker1')
    ticker2 = request.args.get('ticker2')

    # Пока просто возвращаем заглушку
    return jsonify({
        'ticker1': ticker1,
        'ticker2': ticker2,
        'correlation': 0.85  # Потом заменим на реальную
    })

if __name__ == '__main__':
    app.run(debug=True)
