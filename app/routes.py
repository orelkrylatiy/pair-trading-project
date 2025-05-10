from flask import Blueprint, request, jsonify
from .services import calculate_correlation

main = Blueprint('main', __name__)

@main.route('/api/correlation')
def correlation():
    ticker1 = request.args.get('ticker1')
    ticker2 = request.args.get('ticker2')
    start_date = request.args.get('start', '2023-01')

    if not ticker1 or not ticker2:
        return jsonify({'error': 'Missing ticker1 or ticker2'}), 400

    result = calculate_correlation(ticker1, ticker2, start_date)
    return jsonify(result)
