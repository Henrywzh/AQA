import dash
from dash import dcc, html
import dash_mantine_components as dmc
import requests
from dash.dependencies import Input, Output
import plotly.graph_objs as go

res = requests.get("http://127.0.0.1:5000/Sector")
_sectors = res.json()

def get_ebitda(sector: str) -> list[str]:
    res = requests.get(f"http://127.0.0.1:5000/EBITDA?Sector={sector}")
    return res.json() if res.status_code == 200 else []

app = dash.Dash(__name__)

app.layout = dmc.MantineProvider(
    children=[
        html.H2("Sector EBITDA Distribution"),

        dmc.MultiSelect(
            id="sector-selector",
            label="Select Sectors:",
            data=_sectors,
            value=["Technology"],
            placeholder="Choose sectors...",
            clearable=True,
            searchable=True,
        ),

        dcc.Graph(id="ebitda-pie-chart")
    ]
)

@app.callback(
    Output("ebitda-pie-chart", "figure"),
    Input("sector-selector", "value")
)
def update_pie_chart(selected_sectors):
    if not selected_sectors:
        return go.Figure()  # return blank chart if no selection

    # Aggregate EBITDA across all selected sectors
    labels = []
    values = []

    for sector in selected_sectors:
        ebitda_list = get_ebitda(sector)
        total_ebitda = sum(ebitda_list)
        labels.append(sector)
        values.append(total_ebitda)

    # Create pie chart
    fig = go.Figure(data=[
        go.Pie(labels=labels, values=values, hole=0.3)
    ])
    fig.update_layout(title="EBITDA Contribution by Sector")

    return fig

if __name__ == "__main__":
    app.run(debug=True)