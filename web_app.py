from flask import Flask, request, jsonify, render_template
from api_worker import Weather, BadWeatherModel, MyError
from visualisation import generate_weather_plot
from pprint import pprint
from visualisation import create_dash_app, global_weather_data

app = Flask(__name__)
dash_app = create_dash_app(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('route.html')


@app.route('/', methods=['POST'])
def index_post():
    global global_weather_data
    request_data = request.form
    forecast_days_num = int(request_data[
        'forecast-days-num']) if 'forecast-days-num' in request_data else 1
    cities_data = {
        'startpoint': request_data['startpoint'],
        'endpoint': request_data['endpoint']}
    try:
        processed_data = process_data(
            cities_data, days_nums=forecast_days_num)

        is_bad_weather_at_start = "неприятная" if processed_data[
            'is_bad_weather_at_start'] else "приемлимая"
        is_bad_weather_at_end = "неприятная" if processed_data[
            'is_bad_weather_at_end'] else "приемлимая"

        global_weather_data = {
            'start_weather': processed_data['start_weather'],
            'end_weather': processed_data['end_weather']
        }
        pprint(global_weather_data)

        return render_template(
            'personal.html',
            start_status=is_bad_weather_at_start,
            end_status=is_bad_weather_at_end,
            start_city=request_data['startpoint'],
            end_city=request_data['endpoint'],
            weather_data=global_weather_data
        )
    except MyError as e:
        return render_template('on_error.html', error=e.name, error_desc=e.desc)
    # except Exception as e:
    #     return render_template('on_error.html', error=e, desc=None)


def process_data(cities_data, days_nums=5):
    city_start = Weather(cities_data['startpoint'])
    city_end = Weather(cities_data['endpoint'])

    start_forecast = city_start.get_forecast(days_nums)
    end_forecast = city_end.get_forecast(days_nums)

    return {
        'start_weather': start_forecast,
        'end_weather': end_forecast,
        'is_bad_weather_at_start': BadWeatherModel.is_weather_bad(start_forecast[0]),
        'is_bad_weather_at_end': BadWeatherModel.is_weather_bad(end_forecast[0]),
    }


if __name__ == '__main__':
    app.run(debug=True)
