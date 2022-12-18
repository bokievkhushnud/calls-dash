
import os
import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import pandas as pd
from dash import Input, Output


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets

)
server = app.server

app.title = "Dash"

df = pd.read_excel(
    "assets/dashboard.xlsx",
)

df_dt_grouped = df.groupby("Date")["Outcome"].count()


def partA(outcome):
    figure = go.Figure()

    totac = df.groupby("Date")["Outcome"].count()
    totsuc = df[df["Outcome"] == "Success"].groupby("Date")["Outcome"].count()
    totnsuc = df[df["Outcome"] == "Failure"].groupby("Date")["Outcome"].count()
    ratio = totac[totsuc.index]

    figure.add_trace(trace=go.Line(
        x=totac.index, y=totac.values, name="Total calls"))
    figure.add_trace(trace=go.Line(
        x=totsuc.index, y=totsuc.values, name="Success"))
    figure.add_trace(trace=go.Line(
        x=totnsuc.index, y=totnsuc.values, name="Non Success"))

    if outcome == "Success":
        pass
    else:
        figure.add_trace(
            trace=go.Line(
                x=totsuc.index, y=totsuc.values * 100 / ratio, name="Ration success/total calls"
            )
        )

    figure["layout"][
        "title"
    ] = "We want to see this data in a graph with a time series legend. Then we want to see in the same graph the ratio of success /total calls as a function of date."
    figure["layout"]["xaxis"]["title"] = "Date"
    figure["layout"]["yaxis"]["title"] = "Number of calls or ratio"
    figure["layout"]["legend_title"] = "Time series"

    return figure


def partB():
    figure = go.Figure()

    a = df[df["Outcome"] == "Success"].groupby("State")["Outcome"].count()
    b = df[df["Outcome"] == "Failure"].groupby("State")[
        "Outcome"].count()

    # a, b = partB()
    figure.add_trace(
        trace=go.Bar(
            x=a.index,
            y=a.values,
            name="Success",
        )
    )
    figure.add_trace(
        trace=go.Bar(
            x=b.index,
            y=b.values,
            name="Failure",
        )
    )

    figure["layout"][
        "title"
    ] = "We want to see another graph that presents the success and failure by State in the form of a bar graph."
    figure["layout"]["xaxis"]["title"] = "Date"
    figure["layout"]["yaxis"]["title"] = "Number of calls"
    figure["layout"]["legend_title"] = "Time series"

    return figure


def partC():
    figure = go.Figure()
    success_failed = df.groupby("Outcome")["Outcome"].count()

    figure.add_trace(
        trace=go.Pie(
            labels=success_failed.index,
            values=success_failed.values,
        ),
    )

    figure["layout"][
        "title"
    ] = "We want to see a piechart that displays failure-success-timeout as a percentage"
    figure["layout"]["legend_title"] = "Labels"

    return figure


def partD():
    totac = df.groupby("State")["Outcome"].count()
    totsuc = df[df["Outcome"] == "Success"].groupby("State")["Outcome"].count()

    state_success = (totsuc / totac * 100).sort_values(ascending=False)
    highest_state = state_success.idxmax()
   
    return  html.Div(children=
    [  html.P("The most Successful State"),
        html.H1(highest_state),
    ],
    className="menu1"
    )


def partE():
    figure = go.Figure()

    totac = df.groupby("State")["Outcome"].count()
    totsuc = df[df["Outcome"] == "Success"].groupby("State")["Outcome"].count()

    figure.add_trace(
        go.Pie(
            labels=totac.index,
            values=totac.values,
            textinfo="none",
            name="total calls",
            hole=0.6,
        ),
    )

    figure.add_trace(
        go.Pie(
            labels=totsuc.index,
            values=totsuc.values,
            textinfo="none",
            name="success calls",
            hole=0.45,
        ),
    )
    figure.data[0].domain = {"x": [0, 1], "y": [1, 1]}
    figure.data[1].domain = {"x": [0, 1], "y": [0.22, 0.78]}
    figure.update_traces(hoverinfo="label+percent+name")

    figure["layout"][
        "title"
    ] = "We also want to see a double piechart that displays the total number of actions/ State and number of success / state ."
    figure["layout"]["legend_title"] = "Labels"

    return figure


def partF():
    figure = go.Figure()

    df["Success"] = df["Outcome"].apply(
        lambda outcome: 1 if outcome == "Success" else 0
    )

    time_period = df[df.Success == 1]

    time_period["Time_Period"] = time_period["Time_Period"].apply(
        lambda time_period: "0" + time_period
        if len(time_period.split("h")[0]) == 1
        else time_period
    )

    x = time_period.groupby("Time_Period")["Success"].sum()
    figure.add_trace(
        go.Bar(
            x=x.index,
            y=x.values,
            name="Time Period",
        )
    )

    figure["layout"][
        "title"
    ] = "We want to know the number of succes by Time_Period (be careful with the ordering)"
    figure["layout"]["xaxis"]["title"] = "Hours/Time"
    figure["layout"]["yaxis"]["title"] = "Success calls"

    return figure


def filterDate(state, outcome, startDate, endDate):
    global df, df_dt_grouped

    df = pd.read_excel(
        "assets/dashboard.xlsx",
    )

    if state == "All" and outcome == "All":
        df = df[(df.Date >= startDate) & (df.Date <= endDate)]
    elif state == "All":
        df = df[(df.Date >= startDate) & (df.Date <= endDate)]
        df = df[df.Outcome == outcome]
    elif outcome == "All":
        df = df[(df.Date >= startDate) & (df.Date <= endDate)]
        df = df[df.State.isin(state)]
    else:
        df = df[(df.Date >= startDate) & (df.Date <= endDate)]
        df = df[df.State.isin(state)]
        df = df[df.Outcome == outcome]

    df_dt_grouped = df.groupby("Date")["Outcome"].count()


fig_names = ["A", "B", "C", "D", "E", "F"]


fig_plot = html.Div(id="fig_plot", style={"margin": "20px"},
children=[
    dcc.Graph(id="g1"),
    dcc.Graph(id="g2"),
    html.Div(
      children=[
        dcc.Graph(id="g3"),
        html.Div(id="g4" ),
      ],
      className="group_g"
    ),
    dcc.Graph(id="g5"),
    dcc.Graph(id="g6"),
],
)

app.layout = html.Div(
    [
        html.Div(
            children=[
                html.P(children="☎️", className="header-emoji"),
                html.H1(
                    children="Calls Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the success/fail calls in the US",
                    className="header-description",
                ),
            ],
            className="header",
        ),

        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Outcome", className="menu-title"),
                        dcc.Dropdown(
                            id="outcome-filter",
                            options=["All", "Success", "Failure"],
                            value="All",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="State", className="menu-title"),
                        dcc.Dropdown(
                            id="state-filter",
                            multi=True,
                            options=df.State.unique(),
                            value="All",
                            className="dropdown",
                            placeholder="All"
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            start_date=df.Date.min().date(),
                            end_date=df.Date.max().date(),
                            min_date_allowed=df.Date.min().date(),
                            max_date_allowed=df.Date.max().date(),
                            display_format="DD/MM/YYYY",
                        ),
                    ],
                ),
            ],
            className="menu",
            id='nav',
        ),
        fig_plot,

    ]
)


@app.callback(
    [Output("g1", "figure"),
    Output("g2", "figure"),
    Output("g3", "figure"),
    Output("g4", "children"),
    Output("g5", "figure"),
    Output("g6", "figure"),
    ],
    [
     Input("outcome-filter", "value"),
     Input("state-filter", "value"),
     Input("date-range", "start_date"),
     Input("date-range", "end_date"),
     ]
)
def update_output(outcome, state, startDate, endDate):

    if state == None or len(state) == 0:
        state = "All"

    filterDate(state, outcome, startDate, endDate)

    return partA(outcome), partB(), partC(), partD(), partE(), partF()

if __name__ == "__main__":
    app.run_server("0.0.0.0", debug=False, port=int(
        os.environ.get('PORT', 8000)))
