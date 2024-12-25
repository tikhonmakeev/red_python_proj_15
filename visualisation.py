from dash import Dash, dcc, html
from flask import Flask, request, render_template, redirect, url_for, jsonify
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import json
import plotly.graph_objects as go

global_weather_data = []


def generate_weather_plot(weather_data, date):
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number+gauge",
        value=weather_data['temperature'],
        title={'text': "Temperature (°C)"},
        gauge={
            'axis': {'range': [-20, 40]},  # Example range
        }

    ))

    fig.add_trace(go.Indicator(
        mode="number+gauge",
        value=weather_data['humidity'],
        title={'text': "Humidity (%)"},
        gauge={
            'axis': {'range': [0, 100]},  # Example range
        }

    ))
    fig.add_trace(go.Indicator(
        mode="number+gauge",
        value=weather_data['rain_chance'],
        title={'text': "Rain Chance (%)"},
        gauge={
            'axis': {'range': [0, 100]},  # Example range
        }

    ))

    fig.update_layout(
        title=f"Weather Forecast for {date}",
        grid={'rows': 1, 'columns': 3, 'pattern': 'independent'},


    )
    return fig


def create_dash_app(flask_app):
    dash_app = Dash(__name__, server=flask_app, url_base_pathname='/dash/')

    dash_app.layout = html.Div([
        html.H1("Weather Data Visualization"),
        html.Div(id='graphs-container'),
        dcc.Store(id='weather-data-store', data=global_weather_data)
    ])

    @dash_app.callback(
        Output('graphs-container', 'children'),
        Input('weather-data-store', 'data')
    )
    def update_graphs(weather_data):
        if not weather_data:
            return dash.no_update  # Handle empty data

        graphs = []

        # Iterate through each location's forecast (start and end)
        for location_key in ['start_weather', 'end_weather']:
            if location_key not in weather_data:
                continue  # Location is not in weather_data. Skipping it
            location_data = weather_data[location_key]

            # Iterate through each day's forecast for the current location
            for day_data in location_data:

                date = day_data['date']
                fig = generate_weather_plot(day_data, date)

                # Append a new graph for each day:
                graphs.append(html.Div([
                    html.H2(f"""Forecast for {location_key} on {
                            date}"""),  # Add title for each day
                    dcc.Graph(figure=fig)
                ]))

        return graphs  # Return the list of Divs containing the graphs

    return dash_app
