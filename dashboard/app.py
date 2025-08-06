
import dash
from dash import html, dcc
import pandas as pd
import os

app = dash.Dash(__name__)

def load_data():
    data_path = os.path.join(os.path.dirname(__file__), '../data/sample_pcb_data.csv')
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        return df
    return pd.DataFrame()

df = load_data()

app.layout = html.Div([
    html.H1("CircuitGuard Dashboard"),
    html.P("PCB Fault Detection Status"),
    dcc.Markdown(f"**Total Samples:** {len(df)}"),
    dcc.Markdown(f"**Faulty Detected:** {df['faulty'].sum() if 'faulty' in df.columns else 0}"),
    dcc.Markdown(f"**Non-Faulty:** {(df['faulty'] == 0).sum() if 'faulty' in df.columns else 0}"),
    dcc.Markdown("---"),
    dcc.Markdown("Sample Data Preview:"),
    dcc.Graph(
        figure={
            'data': [
                {'x': df['sample_id'] if 'sample_id' in df.columns else [], 'y': df['faulty'] if 'faulty' in df.columns else [], 'type': 'bar', 'name': 'Faulty'}
            ],
            'layout': {'title': 'Faulty Samples by ID'}
        }
    ) if not df.empty else html.P("No data available.")
])

if __name__ == "__main__":
    app.run(debug=True)
