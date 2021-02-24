import os
from typing import Any, Callable

import flask
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline


class InvalidPayloadError(Exception):
    pass


def create_predict_handler(
    path: str = os.getenv("MODEL_PATH", "data/pipeline.pkl"),
) -> Callable[[flask.Request], flask.Response]:
    """
    This function loads a previously trained model and initialises response labels.

    If then wraps an 'inner' handler function (ensuring above model and response labels
    are in scope for the wrapped function, and that each is initialised exactly once at
    runtime).

    Parameters
    ----------
    path: str
        A path to the target model '.joblib' file.

    Returns
    -------

    """

    model: Pipeline = joblib.load(path)
    statuses = {0: "clear", 1: "heart-disease"}

    def handler(request: flask.Request) -> Any:
        request_json = request.get_json()
        df = pd.DataFrame.from_records([request_json])
        try:
            yh = model.predict(df)
        except ValueError as e:
            raise InvalidPayloadError(e)

        return flask.jsonify(dict(diagnosis=statuses[int(yh[0])]))

    return handler


predict = create_predict_handler()
