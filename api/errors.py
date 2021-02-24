from flask import Blueprint, Response
from .handlers.predict import InvalidPayloadError

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(Exception)
def server_error(error):
    return Response(f"Oops, got an error! {error}", status=500)


@errors.app_errorhandler(InvalidPayloadError)
def client_error(error):
    return Response(f"Encountered client {error}", status=400)