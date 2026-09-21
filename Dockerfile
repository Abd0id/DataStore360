ARG AIRFLOW_VERSION=2.9.2
ARG PYTHON_VERSION=3.10

FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}

ENV AIRFLOW_HOME=/opt/airflow

USER root
COPY requirements.txt /
RUN uv pip install --system -r /requirements.txt
USER airflow
