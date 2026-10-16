import dash
from dash import dcc, html, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from backend.features import engineer_transaction, to_model_frame, PRE_APPROVAL_FEATURES, POST_PROCESSING_FEATURES

# Load performance reports
base_dir = Path(__file__).parent.parent
reports_dir = base_dir / "mlops" / "monitoring" / "reports"

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Generate sample data for demonstration
def generate_sample_data():
    np.random.seed(42)
    n = 1000
    df = pd.DataFrame({
        "Date": pd.date_range(start="2024-01-01", periods=n, freq="h"),
        "Transaction_Type": np.random.choice(["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"], n),
        "Amount": np.random.exponential(1000, n).round(2),
        "Sender_Balance": np.random.exponential(5000, n).round(2),
        "Receiver_Balance": np.random.exponential(3000, n).round(2),
        "Is_Fraud": np.random.choice([0, 1], n, p=[0.99, 0.01]),
        "Hour": np.random.randint(0, 24, n),
    })
    return df

# Generate data once
df = generate_sample_data()

# Load performance metrics
def load_performance_metrics():
    metrics = {
        "pre_approval": {
            "accuracy": 0.9992,
            "precision": 0.7779,
            "recall": 0.5435,
            "f1": 0.6399,
        },
        "post_processing": {
            "accuracy": 0.9999,
            "precision": 1.0,
            "recall": 0.9933,
            "f1": 0.9966,
        }
    }
    return metrics

metrics = load_performance_metrics()

# Dashboard Layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("🛡️ FraudGuard AI", className="text-white mb-2"),
            html.P("Business Intelligence Dashboard", className="text-white-50 mb-0"),
        ], width=12, className="p-4 bg-primary")
    ], className="mb-4"),

    # KPI Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Total Transactions", className="text-muted mb-2"),
                    html.H3(f"{len(df):,}", className="mb-0"),
                    html.Small("Last 30 days", className="text-success"),
                ])
            ], className="bg-dark border-0")
        ], width=3, className="mb-4"),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Fraud Cases", className="text-muted mb-2"),
                    html.H3(f"{df['Is_Fraud'].sum():,}", className="mb-0 text-danger"),
                    html.Small(f"{df['Is_Fraud'].mean()*100:.2f}% rate", className="text-warning"),
                ])
            ], className="bg-dark border-0")
        ], width=3, className="mb-4"),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Total Amount", className="text-muted mb-2"),
                    html.H3(f"${df['Amount'].sum():,.0f}", className="mb-0"),
                    html.Small("Processed", className="text-info"),
                ])
            ], className="bg-dark border-0")
        ], width=3, className="mb-4"),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Model Accuracy", className="text-muted mb-2"),
                    html.H3("99.99%", className="mb-0 text-success"),
                    html.Small("Post-processing", className="text-success"),
                ])
            ], className="bg-dark border-0")
        ], width=3, className="mb-4"),
    ]),

    # Filters
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📊 Filters", className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Transaction Type"),
                            dcc.Dropdown(
                                id="type-filter",
                                options=[{"label": "All", "value": "all"}] + [{"label": t, "value": t} for t in df["Transaction_Type"].unique()],
                                value="all",
                                className="mb-2"
                            ),
                        ], width=3),
                        dbc.Col([
                            html.Label("Min Amount"),
                            dcc.Slider(
                                id="amount-filter",
                                min=0,
                                max=10000,
                                value=0,
                                marks={0: "0", 2500: "2.5K", 5000: "5K", 7500: "7.5K", 10000: "10K"},
                                className="mb-2"
                            ),
                        ], width=3),
                        dbc.Col([
                            html.Label("Hour Range"),
                            dcc.RangeSlider(
                                id="hour-filter",
                                min=0,
                                max=23,
                                value=[0, 23],
                                marks={i: str(i) for i in range(0, 24, 6)},
                                className="mb-2"
                            ),
                        ], width=3),
                        dbc.Col([
                            html.Label("Show Fraud Only"),
                            dbc.Switch(
                                id="fraud-filter",
                                value=False,
                                label="Fraud Only",
                                className="mb-2"
                            ),
                        ], width=3),
                    ]),
                ])
            ], className="bg-dark border-0")
        ], width=12, className="mb-4"),
    ]),

    # Charts Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📈 Fraud Trends Over Time"),
                dbc.CardBody([
                    dcc.Graph(id="trend-chart")
                ])
            ], className="bg-dark border-0")
        ], width=8, className="mb-4"),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🥧 Fraud by Transaction Type"),
                dbc.CardBody([
                    dcc.Graph(id="type-chart")
                ])
            ], className="bg-dark border-0")
        ], width=4, className="mb-4"),
    ]),

    # Charts Row 2
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("💰 Amount Distribution"),
                dbc.CardBody([
                    dcc.Graph(id="amount-chart")
                ])
            ], className="bg-dark border-0")
        ], width=6, className="mb-4"),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🕐 Fraud by Hour of Day"),
                dbc.CardBody([
                    dcc.Graph(id="hour-chart")
                ])
            ], className="bg-dark border-0")
        ], width=6, className="mb-4"),
    ]),

    # Model Performance Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🤖 Model Performance Comparison"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6("Pre-Approval Model", className="text-info mb-3"),
                            html.P(f"Accuracy: {metrics['pre_approval']['accuracy']:.4f}"),
                            html.P(f"Precision: {metrics['pre_approval']['precision']:.4f}"),
                            html.P(f"Recall: {metrics['pre_approval']['recall']:.4f}"),
                            html.P(f"F1-Score: {metrics['pre_approval']['f1']:.4f}"),
                            dbc.Progress([
                                dbc.Progress(value=metrics['pre_approval']['accuracy']*100, label="Accuracy", color="info"),
                                dbc.Progress(value=metrics['pre_approval']['precision']*100, label="Precision", color="success"),
                                dbc.Progress(value=metrics['pre_approval']['recall']*100, label="Recall", color="warning"),
                            ], className="mt-3"),
                        ], width=6),
                        dbc.Col([
                            html.H6("Post-Processing Model", className="text-success mb-3"),
                            html.P(f"Accuracy: {metrics['post_processing']['accuracy']:.4f}"),
                            html.P(f"Precision: {metrics['post_processing']['precision']:.4f}"),
                            html.P(f"Recall: {metrics['post_processing']['recall']:.4f}"),
                            html.P(f"F1-Score: {metrics['post_processing']['f1']:.4f}"),
                            dbc.Progress([
                                dbc.Progress(value=metrics['post_processing']['accuracy']*100, label="Accuracy", color="success"),
                                dbc.Progress(value=metrics['post_processing']['precision']*100, label="Precision", color="success"),
                                dbc.Progress(value=metrics['post_processing']['recall']*100, label="Recall", color="success"),
                            ], className="mt-3"),
                        ], width=6),
                    ])
                ])
            ], className="bg-dark border-0")
        ], width=12, className="mb-4"),
    ]),

    # Data Table
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📋 Transaction Data"),
                dbc.CardBody([
                    dash_table.DataTable(
                        id="data-table",
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.head(100).to_dict("records"),
                        page_size=20,
                        style_table={"overflowX": "auto"},
                        style_header={"backgroundColor": "#2c3e50", "color": "white"},
                        style_cell={"backgroundColor": "#1a1a1a", "color": "white"},
                        style_data_conditional=[
                            {
                                "if": {"filter_query": "{Is_Fraud} = 1"},
                                "backgroundColor": "#721c24",
                                "color": "white",
                            }
                        ],
                    )
                ])
            ], className="bg-dark border-0")
        ], width=12, className="mb-4"),
    ]),

    # Footer
    dbc.Row([
        dbc.Col([
            html.Footer([
                html.P("FraudGuard AI Business Intelligence Dashboard", className="text-center text-muted mb-0"),
                html.P("Generated with Plotly Dash | Professional Analytics", className="text-center text-muted small"),
            ])
        ], width=12, className="p-3")
    ]),

], fluid=True, className="bg-dark min-vh-100")

# Callbacks
@app.callback(
    [Output("trend-chart", "figure"),
     Output("type-chart", "figure"),
     Output("amount-chart", "figure"),
     Output("hour-chart", "figure"),
     Output("data-table", "data")],
    [Input("type-filter", "value"),
     Input("amount-filter", "value"),
     Input("hour-filter", "value"),
     Input("fraud-filter", "value")]
)
def update_charts(type_filter, amount_filter, hour_filter, fraud_filter):
    # Filter data
    filtered_df = df.copy()

    if type_filter != "all":
        filtered_df = filtered_df[filtered_df["Transaction_Type"] == type_filter]

    filtered_df = filtered_df[filtered_df["Amount"] >= amount_filter]

    filtered_df = filtered_df[
        (filtered_df["Hour"] >= hour_filter[0]) &
        (filtered_df["Hour"] <= hour_filter[1])
    ]

    if fraud_filter:
        filtered_df = filtered_df[filtered_df["Is_Fraud"] == 1]

    # Trend chart
    trend_fig = px.line(
        filtered_df.groupby("Date")["Is_Fraud"].sum().reset_index(),
        x="Date",
        y="Is_Fraud",
        title="Fraud Cases Over Time",
        template="plotly_dark"
    )
    trend_fig.update_layout(showlegend=False)

    # Type chart
    type_fig = px.pie(
        filtered_df.groupby("Transaction_Type")["Is_Fraud"].sum().reset_index(),
        values="Is_Fraud",
        names="Transaction_Type",
        title="Fraud Distribution by Type",
        template="plotly_dark"
    )

    # Amount chart
    amount_fig = px.histogram(
        filtered_df,
        x="Amount",
        color="Is_Fraud",
        nbins=50,
        title="Amount Distribution",
        template="plotly_dark",
        color_discrete_map={0: "green", 1: "red"}
    )

    # Hour chart
    hour_fig = px.line(
        filtered_df.groupby("Hour")["Is_Fraud"].mean().reset_index(),
        x="Hour",
        y="Is_Fraud",
        title="Fraud Rate by Hour",
        template="plotly_dark"
    )

    # Data table
    table_data = filtered_df.head(100).to_dict("records")

    return trend_fig, type_fig, amount_fig, hour_fig, table_data

if __name__ == "__main__":
    app.run(debug=True, port=8050)
