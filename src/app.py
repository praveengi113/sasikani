from flask import Flask, render_template, current_app
from src.common.post import Feed

app = Flask(__name__)
"""
@app.route('/')
def index():
    covid_data_log = Feed.from_mongo_all()
    covid_data = Feed.from_mongo()
    cases = covid_data[0]["cases"]
    cured = covid_data[0]["cured"]
    death = covid_data[0]["death"]
    date = covid_data[0]["time"]
    return render_template('cards_try.html', cases=cases, cured=cured, death=death, date=date, log=covid_data_log)
"""


@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run()
