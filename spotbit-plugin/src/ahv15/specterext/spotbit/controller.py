from flask import redirect, render_template, request, url_for
from flask import current_app as app

from cryptoadvance.specter.specter import Specter
from .service import SpotbitService

from datetime import datetime


spotbit_endpoint = SpotbitService.blueprint


def ext() -> SpotbitService:
    ''' convenience for getting the extension-object'''
    return app.specter.ext["spotbit"]


def specter() -> Specter:
    ''' convenience for getting the specter-object'''
    return app.specter


@spotbit_endpoint.route("/")
def index():
    service = ext()
    status_info = service.status_info()
    return render_template(
        "spotbit/index.jinja",  status=status_info
    )


@spotbit_endpoint.route("/", methods=["POST"])
def index_post():
    service = ext()
    info = request.form.get('pair', "None")
    print("Test")
    print(info)
    if (info == ""):
        service.remove_db()
    else:
        service.remove_exchange(info.strip('][').split(', '))
    status_info = service.status_info()
    return render_template(
        "spotbit/index.jinja",  status=status_info
    )


@spotbit_endpoint.route("/hist/<currency>/<exchange>/<date_start>/<date_end>")
def historical_exchange_rate(currency, exchange, date_start, date_end):
    service = ext()
    return (service.historical_exchange_rate(currency, exchange, date_start, date_end))


@spotbit_endpoint.route("/now/<currency>/<exchange>")
def current_exchange_rate(currency, exchange):
    service = ext()
    return (service.current_exchange_rate(currency, exchange))


@spotbit_endpoint.route("/settings", methods=["GET"])
def settings_get():
    return render_template(
        "spotbit/settings.jinja",
    )


@spotbit_endpoint.route("/settings", methods=["POST"])
def settings_post():
    exchange = request.form.get('exchange', "None")
    currency1 = request.form.get('currency1', "None")
    currency2 = request.form.get('currency2', "None")
    currency3 = request.form.get('currency3', "None")
    currency4 = request.form.get('currency4', "None")
    currency5 = request.form.get('currency5', "None")
    currency6 = request.form.get('currency6', "None")
    currency7 = request.form.get('currency7', "None")
    currency8 = request.form.get('currency8', "None")
    currency9 = request.form.get('currency9', "None")
    start_date = request.form.get('start_date', "None")
    frequencies = request.form.get('frequencies', "1m")
    service = ext()
    service.init_table([exchange.lower()], [currency1, currency2, currency3, currency4, currency5, currency6,
                       currency7, currency8, currency9], frequencies, start_date)
    return redirect(url_for(f"{ SpotbitService.get_blueprint_name()}.settings_get"))
