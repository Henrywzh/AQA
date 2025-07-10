from flask import Flask, request, jsonify
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

if __name__ == '__main__':
    main()
