# ===============================
# IMPORTS
# ===============================
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# ===============================
# INIT APP
# ===============================
app = Dash(__name__)
server = app.server
# ===============================
# LOAD DATA
# ===============================
errors_df = pd.read_csv("data/system_errors.csv")
finance_df = pd.read_csv("data/financial_transactions.csv")

errors_df["created_at"] = pd.to_datetime(errors_df["created_at"])
finance_df["created_at"] = pd.to_datetime(finance_df["created_at"])

# ===============================
# STYLES
# ===============================
CARD_STYLE = {
    "padding": "20px",
    "borderRadius": "10px",
    "color": "white",
    "width": "30%",
    "textAlign": "center",
    "fontSize": "18px",
    "fontWeight": "bold"
}

# ===============================
# LAYOUT
# ===============================
app.layout = html.Div(style={"display": "flex", "backgroundColor": "#0E1117"}, children=[

    # ===============================
    # SIDEBAR
    # ===============================
    html.Div([
        html.H2("📊 Filters", style={"color": "white"}),

        dcc.Dropdown(
            id="mode",
            options=[
                {"label": "System Errors", "value": "errors"},
                {"label": "Financial", "value": "finance"}
            ],
            value="finance"
        ),

        html.Br(),

        dcc.DatePickerRange(
            id="date_filter",
            start_date=finance_df["created_at"].min(),
            end_date=finance_df["created_at"].max(),
            display_format="YYYY-MM-DD"
        )

    ], style={
        "width": "20%",
        "padding": "20px",
        "backgroundColor": "#161B22"
    }),

    # ===============================
    # MAIN AREA
    # ===============================
    html.Div([

        html.H1("📊 Monitoring Dashboard", style={"color": "white"}),

        # KPIs
        html.Div(id="kpis", style={
            "display": "flex",
            "justifyContent": "space-between",
            "marginBottom": "30px"
        }),

        # GRÁFICOS
        html.Div([
            dcc.Graph(id="main_graph", style={"width": "48%"}),
            dcc.Graph(id="secondary_graph", style={"width": "48%"})
        ], style={"display": "flex", "justifyContent": "space-between"}),

        html.Div([
            dcc.Graph(id="third_graph")
        ], style={"marginTop": "30px"})

    ], style={"width": "80%", "padding": "20px"})

])

# ===============================
# CALLBACK
# ===============================
@app.callback(
    [
        Output("main_graph", "figure"),
        Output("secondary_graph", "figure"),
        Output("third_graph", "figure"),
        Output("kpis", "children")
    ],
    [
        Input("mode", "value"),
        Input("date_filter", "start_date"),
        Input("date_filter", "end_date")
    ]
)
def update_dashboard(mode, start_date, end_date):

    # ===============================
    # ESCOLHA DO DATAFRAME
    # ===============================
    if mode == "finance":
        df = finance_df.copy()
    else:
        df = errors_df.copy()

    # ===============================
    # FILTRO DE DATA
    # ===============================
    df = df[
        (df["created_at"] >= start_date) &
        (df["created_at"] <= end_date)
    ]

    # ===============================
    # FINANCE
    # ===============================
    if mode == "finance":

        total = df["amount"].sum()
        avg = df["amount"].mean()
        high_risk = df[df["risk_level"] == "High"].shape[0]

        kpis = [
            html.Div(f"💰 Total: ${total:,.0f}", style={**CARD_STYLE, "backgroundColor": "#1f77b4"}),
            html.Div(f"📊 Avg: ${avg:,.2f}", style={**CARD_STYLE, "backgroundColor": "#2ca02c"}),
            html.Div(f"⚠️ High Risk: {high_risk}", style={**CARD_STYLE, "backgroundColor": "#d62728"})
        ]

        # 📈 Volume ao longo do tempo
        daily = df.groupby(df["created_at"].dt.date)["amount"].sum().reset_index()

        fig1 = px.line(daily, x="created_at", y="amount",
                       title="Financial Volume Over Time")
        fig1.update_layout(template="plotly_dark")

        # ⚠️ Risco
        fig2 = px.bar(
            df,
            x="risk_level",
            color="risk_level",
            title="Risk Distribution",
            category_orders={"risk_level": ["Low", "Medium", "High"]},
            color_discrete_map={
                "Low": "#2ECC71",
                "Medium": "#F1C40F",
                "High": "#E74C3C"
            }
        )
        fig2.update_layout(template="plotly_dark")

        # 🏆 TOP 5 categorias
        top_cat = df.groupby("category")["amount"].sum().nlargest(5).reset_index()

        fig3 = px.bar(
            top_cat,
            x="amount",
            y="category",
            orientation="h",
            title="Top 5 Categories by Revenue",
            color="amount",
            color_continuous_scale="Blues"
        )
        fig3.update_layout(template="plotly_dark")

    # ===============================
    # ERRORS
    # ===============================
    else:

        total = len(df)
        critical = df[df["severity"] == "Critical"].shape[0]
        open_ = df[df["status"] != "Resolved"].shape[0]

        kpis = [
            html.Div(f"🐞 Total: {total}", style={**CARD_STYLE, "backgroundColor": "#1f77b4"}),
            html.Div(f"🔥 Critical: {critical}", style={**CARD_STYLE, "backgroundColor": "#E74C3C"}),
            html.Div(f"⏳ Open: {open_}", style={**CARD_STYLE, "backgroundColor": "#F39C12"})
        ]

        # 📉 Erros ao longo do tempo
        daily = df.groupby(df["created_at"].dt.date).size().reset_index(name="count")

        fig1 = px.line(daily, x="created_at", y="count",
                       title="Errors Over Time")
        fig1.update_layout(template="plotly_dark")

        # 🔥 Severidade
        fig2 = px.bar(
            df,
            x="severity",
            color="severity",
            title="Error Severity",
            category_orders={"severity": ["Low", "Medium", "High", "Critical"]},
            color_discrete_map={
                "Low": "#2ECC71",
                "Medium": "#F1C40F",
                "High": "#E67E22",
                "Critical": "#E74C3C"
            }
        )
        fig2.update_layout(template="plotly_dark")

        # 🏆 TOP 5 módulos
        top_mod = df["module"].value_counts().nlargest(5).reset_index()
        top_mod.columns = ["module", "count"]

        fig3 = px.bar(
            top_mod,
            x="count",
            y="module",
            orientation="h",
            title="Top 5 Modules with Most Errors",
            color="count",
            color_continuous_scale="Reds"
        )
        fig3.update_layout(template="plotly_dark")

    return fig1, fig2, fig3, kpis


# ===============================
# RUN APP
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)