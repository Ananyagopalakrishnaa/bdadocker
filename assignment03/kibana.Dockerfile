FROM python:3.9
RUN pip install elasticsearch matplotlib pandas
COPY kibana_visualization.py /
CMD ["python", "./kibana_visualization.py"]
