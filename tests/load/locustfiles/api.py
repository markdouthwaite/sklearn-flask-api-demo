import random
from dataclasses import dataclass, asdict
from locust import HttpUser, between, task


random.seed(42)


@dataclass
class Payload:
    # values derived from https://www.kaggle.com/ronitf/heart-disease-uci
    # and https://archive.ics.uci.edu/ml/datasets/heart+disease
    sex: int = random.randint(0, 1)
    cp: int = random.randint(0, 3)
    restecg: int = random.randint(0, 1)
    ca: int = random.randint(0, 3)
    slope: int = random.randint(0, 2)
    thal: int = random.randint(0, 3)
    age: int = random.randint(0, 120)
    trestbps: int = random.randint(90, 200)
    chol: int = random.randint(100, 600)
    fbs: int = random.randint(0, 1)
    thalach: int = random.randint(60, 200)
    exang: int = random.randint(0, 1)
    oldpeak: float = random.random() * 7


def iter_random_valid_payloads() -> dict:
    while True:
        yield asdict(Payload())


def iter_random_invalid_payloads() -> dict:
    fields = list(asdict(Payload()).keys())
    while True:
        field = random.choice(fields)
        payload = asdict(Payload())
        # missing field
        del payload[field]
        yield payload


class RandomizedUser(HttpUser):

    # wait between requests from one user for between 1 and 5 seconds.
    wait_time = between(1, 5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valid_payloads = iter_random_valid_payloads()
        self.invalid_payloads = iter_random_invalid_payloads()

    @task(4)
    def get_diagnosis_with_valid_payload(self):
        self.client.post("/predict", json=next(self.valid_payloads))

    @task(1)
    def get_diagnosis_with_invalid_payload(self):
        payload = next(self.invalid_payloads)
        with self.client.post(
            "/predict", json=payload, catch_response=True
        ) as response:
            if response.status_code != 400:
                response.failure(
                    f"Wrong response. Expected status code 400, "
                    f"got {response.status_code}"
                )
            else:
                response.success()
