import urllib.request, json
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from flask import Flask, render_template, request
from flaskcovid import app

API_URL = "https://covid19.mathdro.id/api"
DEFAULT_ENCODING = "utf-8"


def get_countries():
    countries_url = API_URL + "/countries"
    response = urllib.request.urlopen(countries_url)
    data = json.loads(response.read())
    countries = [("", "Global")]
    # print(data["countries"])
    for country in data["countries"]:
        countries.append((country["name"], country["name"]))
        # print(f'country: {country["name"]}')
    return countries


def get_daily_data(url):
    response = urllib.request.urlopen(API_URL + "/daily")
    data = json.loads(response.read())
    dailyData = []
    for daily in data:
        dailyData.append(
            (
                daily["reportDate"],
                daily["confirmed"]["total"],
                daily["recovered"]["total"],
                daily["deaths"]["total"],
            )
        )
        # print(            f'{daily["reportDate"]} : {daily["confirmed"]["total"]}, {daily["recovered"]["total"]}, {daily["deaths"]["total"]}'        )
    return dailyData


class Form(FlaskForm):
    # countriesdata = [("", "Global"), ("US", "US")]
    countriesdata = get_countries()
    # print(type(countriesdata[0]))
    countries = SelectField("Countries", choices=countriesdata)
    submit = SubmitField(" GO ")


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    form = Form()
    url = API_URL
    if request.method == "POST":
        country = form.countries.data
        if country and country != "":
            url = API_URL + "/countries/" + country
    response = urllib.request.urlopen(url)
    json_response = response.read()

    data = json.loads(json_response)
    if data:
        confirmed = data["confirmed"]["value"]
        recovered = data["recovered"]["value"]
        deaths = data["deaths"]["value"]
        print(
            f'url: {url} - confirmed: {data["confirmed"]["value"]}, recovered: {data["recovered"]["value"]}, deaths: {data["deaths"]["value"]}'
        )
    # TODO: work on Daily chart
    # daily_data = get_daily_data(url)

    return render_template(
        "home.html", confirmed=confirmed, recovered=recovered, deaths=deaths, form=form,
    )


@app.route("/about")
def about():
    return render_template("about.html", title="About")
