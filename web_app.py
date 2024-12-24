from flask import Flask, request, jsonify, render_template
from api_worker import Weather, BadWeatherModel, MyError
from visualisation import generate_weather_plot
from pprint import pprint

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('route.html')


@app.route('/', methods=['POST'])
def index_post():
    request_data = request.form
    try:
        processed_data = process_data(request_data)

        start_plot = generate_weather_plot(processed_data['start_weather'])
        end_plot = generate_weather_plot(processed_data['end_weather'])
        return f"<h2>Start Point Weather</h2>{start_plot}<h2>End Point Weather</h2>{end_plot}"

        is_bad_weather_at_start = "неприятная" if processed_data[
            'is_bad_weather_at_start'] else "приемлимая"
        is_bad_weather_at_end = "неприятная" if processed_data[
            'is_bad_weather_at_end'] else "приемлимая"
        return render_template('personal.html', start_status=is_bad_weather_at_start, end_status=is_bad_weather_at_end,
                               start_city=request_data['startpoint'], end_city=request_data['endpoint'])
    except MyError as e:
        return render_template('on_error.html', error=e.name, error_desc=e.desc)
    except Exception as e:
        return render_template('on_error.html', error=e, desc=None)


def process_data(data, days_nums=5):
    city_start = Weather(data['startpoint'])
    city_end = Weather(data['endpoint'])

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
