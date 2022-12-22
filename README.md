# Data Engineer Test 🔥
## Description:
The data science team would like to retrieve information on some blue chip companies.
They found it on YahooFinance webpage and they know that the information that they
want is not available in the YahooFinance’s API.

## Proyecto Web Scraping
📗 libraries Requirements
- bs4
- requests
- pytest
- lxml
- numpy
- pandas
- pycodestyle

📗 Requirements for future improvements 

To use spark on this project it is necessary to have these basic requirements:
- Spark 2.3.0 -- https://archive.apache.org/dist/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.6.tgz
- Python 3.6.8 -- https://www.python.org/downloads/release/python-368/
- Java 1.8.x

📋 Install Python Requirements

To install the python libraries it is recommended to use a virtualenv:
- python -m virtualenv venv
- source venv/bin/activate
- pip install -r requirements.txt

🔧 Path Environments

Consider the following environment variables for future improvements with spark:
- JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
- SPARK_HOME=/usr/local/spark
- PYSPARK_PYTHON=/usr/bin/python3
- PYSPARK_DRIVER_PYTHON=/usr/bin/python3

🚩 Run Tests

Correr las pruebas unitarias y cobertura de código:

- pytest --cov=main src/tests/

✒ Authors ️

- Leonardo Rodrigues de Andrade

📄 Licence

- This project is under the license of Leonardo Rodrigues de Andrade

🤝 Support

Contributions, issues, and feature requests are welcome.