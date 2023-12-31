# -*- coding: utf-8 -*-
"""analysis_dashboard_app.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-QJP00hkEs3DO23d-fZOujpQDpnf65Pg
"""

pip install dash pandas plotly

from google.colab import drive

# Mount Google Drive
drive.mount('/content/gdrive')

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash.exceptions import PreventUpdate
import io

# Initialize the Dash app
app = dash.Dash(__name__)

# Define layout for the dashboard
app.layout = html.Div([
    # Dropdown for file selection
    dcc.Dropdown(
        id='file-dropdown',
        options=[
            {'label': '16MGD Lab Analysis', 'value': '/content/drive/MyDrive/Ideatec DL/DEL/Input/lab_analysis_16MGD.csv'},
            {'label': '25MGD Lab Analysis', 'value': '/content/drive/MyDrive/Ideatec DL/DL/Input/dl_yamuna_vihar_25mgd_lab_analysis.csv'},
            {'label': '16MGD Lab Analysis(FIRST 10 Days)', 'value': '/content/drive/MyDrive/Ideatec DL/DL/Input/16mgd_first_10_days_data.csv'},
            {'label': '25MGD Lab Analysis(FIRST 10 Days)', 'value': '/content/drive/MyDrive/Ideatec DL/DL/Input/25mgd_first_10_days_data.csv'}
        ],
        value=None,
        placeholder="Select a file",
    ),
    # Time Series Plot for TSS
    dcc.Graph(id='time-series-tss'),
    # Time Series Plot for BOD
    dcc.Graph(id='time-series-bod'),
    # Scatter Plot for Applied Dose vs. Flow
    dcc.Graph(id='scatter-plot-dose-flow'),
    # Box Plot for TSS across Stages
    dcc.Graph(id='box-plot-tss-stages'),
    # Box Plot for BOD across Stages
    dcc.Graph(id='box-plot-bod-stages'),
    # Dual-Axis Chart for TSS and BOD
    dcc.Graph(id='dual-axis-chart'),

    # Add a link to open the output in a new page
    html.A('Open Output in New Page', href='/output', target='_blank')
])

def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = io.StringIO(base64.b64decode(content_string).decode('utf-8'))
    df = pd.read_csv(decoded)
    df['date'] = pd.to_datetime(df['date'])
    return df

@app.callback(
    [Output('time-series-tss', 'figure'),
     Output('time-series-bod', 'figure'),
     Output('scatter-plot-dose-flow', 'figure'),
     Output('box-plot-tss-stages', 'figure'),
     Output('box-plot-bod-stages', 'figure'),
     Output('dual-axis-chart', 'figure')],
    [Input('file-dropdown', 'value')]
)
def update_graph(selected_file):
    if selected_file is None:
        raise PreventUpdate

    # Load the data from the selected file
    df = pd.read_csv(selected_file)
    df['date'] = pd.to_datetime(df['date'])

    # Update figures
    fig_tss = px.line(df, x='date', y=['raw_sewage__tss', 'fst__tss'],
                      labels={'value': 'TSS value', 'variable': 'Stage'},
                      title='TSS Trend Over Time',
                      template='plotly_dark')

    fig_bod = px.line(df, x='date', y=['raw_sewage__bod', 'fst__bod'],
                      labels={'value': 'BOD value', 'variable': 'Stage'},
                      title='BOD Trend Over Time',
                      template='plotly_dark')

    fig_dose_flow = px.scatter(df, x='custom_dosing_data__applied_dose_outlet', y='custom_dosing_data__flow',
                               labels={'custom_dosing_data__applied_dose_outlet': 'Applied Dose Outlet',
                                       'custom_dosing_data__flow': 'Flow'},
                               title='Applied Dose vs. Flow',
                               template='plotly_dark')

    fig_tss_stages = px.box(pd.melt(df[['raw_sewage__tss', 'pst_outlet__tss', 'fst__tss']]),
                            x='variable', y='value', labels={'value': 'TSS Value', 'variable': 'Stage'},
                            title='Distribution of TSS Across Stages',
                            template='plotly_dark')

    fig_bod_stages = px.box(pd.melt(df[['raw_sewage__bod', 'pst_outlet__bod', 'fst__bod']]),
                            x='variable', y='value', labels={'value': 'BOD Value', 'variable': 'Stage'},
                            title='Distribution of BOD Across Stages',
                            template='plotly_dark')

    fig_dual_axis = px.line(df, x='date', y=['fst__tss', 'fst__bod'],
                            labels={'value': 'Value', 'variable': 'Stage'},
                            title='Dual-Axis Chart for TSS and BOD',
                            template='plotly_dark')

    return fig_tss, fig_bod, fig_dose_flow, fig_tss_stages, fig_bod_stages, fig_dual_axis

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8051)

'''
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the data from the CSV file
df = pd.read_csv('/content/drive/MyDrive/Ideatec DL/DL/Input/dl_yamuna_vihar_25mgd_lab_analysis.csv')

# Set the date column as datetime type
df['date'] = pd.to_datetime(df['date'])

# Initialize the Dash app
app = dash.Dash(__name__)

# Define layout for the dashboard
app.layout = html.Div([
    # Time Series Plot for TSS
    dcc.Graph(
        id='time-series-tss',
        figure=px.line(df, x='date', y=['raw_sewage__tss', 'fst__tss'],
                       labels={'value': 'TSS value', 'variable': 'Stage'},
                       title='TSS Trend Over Time',
                       template='plotly_dark')
    ),
    # Time Series Plot for BOD
    dcc.Graph(
        id='time-series-bod',
        figure=px.line(df, x='date', y=['raw_sewage__bod', 'fst__bod'],
                       labels={'value': 'BOD value', 'variable': 'Stage'},
                       title='BOD Trend Over Time',
                       template='plotly_dark')
    ),
    # Scatter Plot for Applied Dose vs. Flow
    dcc.Graph(
        id='scatter-plot-dose-flow',
        figure=px.scatter(df, x='custom_dosing_data__applied_dose_outlet', y='custom_dosing_data__flow',
                          labels={'custom_dosing_data__applied_dose_outlet': 'Applied Dose Outlet', 'custom_dosing_data__flow': 'Flow'},
                          title='Applied Dose vs. Flow',
                          template='plotly_dark')
    ),
    # Box Plot for TSS across Stages
    dcc.Graph(
        id='box-plot-tss-stages',
        figure=px.box(pd.melt(df[['raw_sewage__tss', 'pst_outlet__tss', 'fst__tss']]),
                      x='variable', y='value', labels={'value': 'TSS Value', 'variable': 'Stage'},
                      title='Distribution of TSS Across Stages',
                      template='plotly_dark')
    ),
    # Box Plot for BOD across Stages
    dcc.Graph(
        id='box-plot-bod-stages',
        figure=px.box(pd.melt(df[['raw_sewage__bod', 'pst_outlet__bod', 'fst__bod']]),
                      x='variable', y='value', labels={'value': 'BOD Value', 'variable': 'Stage'},
                      title='Distribution of BOD Across Stages',
                      template='plotly_dark')
    ),
    # Dual-Axis Chart for TSS and BOD
    dcc.Graph(
        id='dual-axis-chart',
        figure=px.line(df, x='date', y=['fst__tss', 'fst__bod'],
                       labels={'value': 'Value', 'variable': 'Stage'},
                       title='Dual-Axis Chart for TSS and BOD',
                       template='plotly_dark')
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8051)
'''