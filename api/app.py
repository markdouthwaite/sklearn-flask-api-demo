from flask import Flask, Response, request

from .errors import errors
from .handlers import predict as predict_handler

app = Flask(__name__)
app.register_blueprint(errors)


@app.route("/predict", methods=["POST"])
def predict():
    return predict_handler(request)


# feel free to add as many handlers in here as you like!


@app.route("/health")
def health():
    return Response("OK", status=200)
