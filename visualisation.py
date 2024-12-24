from flask import Flask, request, render_template, redirect, url_for, jsonify
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import json
import plotly.graph_objects as go


def generate_weather_plot(weather_data):
    dates = [day['date'] for day in weather_data]
    temperatures = [day['temperature'] for day in weather_data]
    humidities = [day['humidity'] for day in weather_data]
    rain_chances = [day['rain_chance'] for day in weather_data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=temperatures,
                  mode='lines+markers', name='Temperature (°C)'))
    fig.add_trace(go.Bar(x=dates, y=humidities, name='Humidity (%)'))
    fig.add_trace(go.Bar(x=dates, y=rain_chances, name='Rain Chance (%)'))

    fig.update_layout(
        title="Weather Forecast",
        xaxis_title="Date",
        yaxis_title="Value",
        barmode='group'
    )
    return fig.to_html()
