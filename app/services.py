import okama

def calculate_correlation(ticker1, ticker2, start_date='2023-01'):
    try:
        assets = okama.Assets([ticker1, ticker2], first_date=start_date)
        corr_matrix = assets.correlation_matrix
        corr_value = corr_matrix.loc[ticker1, ticker2]

        return {
            'ticker1': ticker1,
            'ticker2': ticker2,
            'correlation': round(float(corr_value), 4),
            'status': 'ok'
        }
    except Exception as e:
        return {
            'error': str(e),
            'status': 'error'
        }
