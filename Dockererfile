FROM python:3.11-slim@sha256:edaf703dce209d774af3ff768fc92b1e3b60261e7602126276f9ceb0e3a96874

COPY requirements/requirements.txt .
RUN python -m pip install --requirement requirements.txt

COPY pyproject.toml pyproject.toml
COPY src/ src/
RUN python -m pip install .

RUN adduser --disabled-password hermes
USER hermes

CMD [ "python", "-m", "hermes" ]
