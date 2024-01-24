FROM python:3.12-slim@sha256:db7e9284d53f7b827c58a6239b9d2907c33250215823b1cdb7d1e983e70dafa5

COPY requirements/requirements.txt .
RUN python -m pip install --requirement requirements.txt

COPY pyproject.toml pyproject.toml
COPY src/ src/
RUN python -m pip install .

RUN adduser --disabled-password hermes
USER hermes

CMD [ "python", "-m", "hermes" ]
