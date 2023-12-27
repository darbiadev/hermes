FROM python:3.12-slim@sha256:c805c5edcf6005fd72f933156f504525e1da263ffbc3fae6b4940e6c360c216f

COPY requirements/requirements.txt .
RUN python -m pip install --requirement requirements.txt

COPY pyproject.toml pyproject.toml
COPY src/ src/
RUN python -m pip install .

RUN adduser --disabled-password hermes
USER hermes

CMD [ "python", "-m", "hermes" ]
