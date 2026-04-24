import requests


def before_all(context):
    context.base_url = "https://fakestoreapi.com"
    context.session = requests.Session()
    context.timeout = 10


def before_scenario(context, scenario):
    del scenario
    context.response = None


def after_all(context):
    context.session.close()
