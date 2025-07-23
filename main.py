import io
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

@app.route('/DownloadFilteredCSV')
def download_filtered_csv():
    sectors = request.args.getlist('Sector')
    if not sectors:
        return {"error": "No sectors provided"}, 400

    filtered_df = df[df['Sector'].isin(sectors)]

    if filtered_df.empty:
        print("No data matched the selected sectors.")
        return {"error": "No data available for selected sectors"}, 400

    buffer = io.BytesIO()
    filtered_df.to_csv(buffer, index=False)
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name="filtered_sectors.csv"
    )

if __name__ == '__main__':
    main()
