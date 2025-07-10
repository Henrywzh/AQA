from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd


app = Flask(__name__)
CORS(app)

df = pd.read_csv('constituents-financials_csv.csv')

def main():
    app.run(port=5000)

@app.route('/Sector')
def get_sectors():
    res = df.Sector.unique().tolist()

    return jsonify(res)

@app.route('/EBITDA')
def get_ebitda():
    sector = request.args.get('Sector')
    res = df[df['Sector'] == sector]['EBITDA'].dropna().tolist()

    return jsonify(res)

@app.route('/DownloadCSV')
def download_csv():
    return send_file(
        "constituents-financials_csv.csv",
        mimetype='text/csv',
        as_attachment=True,
        download_name='s&p500_data.csv'
    )

if __name__ == '__main__':
    main()
