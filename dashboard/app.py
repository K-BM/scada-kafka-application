# dashboard/app.py
import dash
import sys
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine, text
import logging

logging.basicConfig(level=logging.INFO)

# Use session/connection pool for efficient database connections
try:
    engine = create_engine('postgresql://scada_user:scada_pass@172.31.109.162:5432/scada_db')
    connection = engine.connect()
    logging.info("Successfully connected to PostgreSQL!")
    connection.close()
except Exception as e:
    logging.error(f"Connection failed: {str(e)}")

# Initialize Dash app
app = dash.Dash(__name__)

# Dashboard layout
app.layout = html.Div([
    html.H1("SCADA Sensor Metrics Dashboard", style={'textAlign': 'center'}),
    
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # Update every 30 seconds
        n_intervals=0
    ),
    
    html.Div([
        dcc.Dropdown(
            id='sensor-id-dropdown',
            placeholder='Select Sensor ID',
            options=[],  # Populated dynamically
            style={'width': '50%', 'margin': '10px'}
        ),
        dcc.Dropdown(
            id='metric-dropdown',
            placeholder='Select Metric',
            options=[
                {'label': 'Temperature (°C)', 'value': 'temperature'},
                {'label': 'Pressure (bar)', 'value': 'pressure'},
                {'label': 'Flow Rate (m³/s)', 'value': 'flow_rate'}
            ],
            style={'width': '50%', 'margin': '10px'}
        )
    ], style={'display': 'flex'}),
    
    dcc.Graph(id='sensor-metric-plot'),
    
    html.Div(id='status-update', style={'padding': '20px', 'fontSize': '18px'})
])

# Callback 1: Populate Sensor ID dropdown
@app.callback(
    Output('sensor-id-dropdown', 'options'),
    Input('interval-component', 'n_intervals')
)
def update_sensor_dropdown(n):
    try:
        query = "SELECT DISTINCT sensor_id FROM sensor_data LIMIT 100"
        df = pd.read_sql(query, engine)
        
        if df.empty:
            logging.warning("No sensor IDs found in the database.")
            return [{'label': 'No sensors available', 'value': ''}]
        
        options = [{'label': sid, 'value': sid} for sid in df['sensor_id']]
        logging.info(f"Sensor dropdown populated with: {options[0]['label']}")
        return options
    except Exception as e:
        logging.error(f"Error fetching sensor IDs: {str(e)}")
        return []

# Callback 2: Update plot and status
@app.callback(
    [Output('sensor-metric-plot', 'figure'),
     Output('status-update', 'children')],
    [Input('interval-component', 'n_intervals')],
    [State('sensor-id-dropdown', 'value'),
     State('metric-dropdown', 'value')]
)
def update_plot(n, selected_sensor, selected_metric):
    if not selected_sensor or not selected_metric:
        return px.line(title="Select a Sensor and Metric"), ""
    
    try:
        # Validate column name to prevent SQL injection
        if selected_metric not in ['temperature', 'pressure', 'flow_rate']:
            raise ValueError("Invalid metric selected")

        # Inject the column name safely (do not use this for values)
        query = f"""
            SELECT timestamp, {selected_metric}, status 
            FROM sensor_data 
            WHERE sensor_id = :sensor_id
            ORDER BY timestamp ASC
            LIMIT 500
        """
        df = pd.read_sql(text(query), engine, params={'sensor_id': selected_sensor})
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        print(df.head())
        print(df.columns)

        fig = px.line(
            df, x='timestamp', y=selected_metric,
            title=f"{selected_metric.capitalize()} Over Time (Sensor: {selected_sensor})"
        )
        
        latest_status = df.iloc[-1]['status']
        status_text = html.Span(
            f"Latest Status for {selected_sensor}: {latest_status}",
            style={'color': 'red' if latest_status == 'ALARM' else 'green'}
        )
        
        return fig, status_text
    except Exception as e:
        logging.error(f"Error updating plot: {e}")
        return px.line(title="Error"), f"Error: {str(e)}"

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
