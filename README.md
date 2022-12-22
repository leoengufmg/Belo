# Data Engineer Test 🔥
## Description:
The data science team would like to retrieve information on some blue chip companies.
They found it on YahooFinance webpage and they know that the information that they
want is not available in the YahooFinance’s API.

## Proyecto Web Scraping
📗 libraries Requirements
- bs4: for scrap purpose
- requests: for scrap purpose
- pytest: develop unit test
- lxml: for scrap purpose
- numpy: work with data frame
- pandas: work with data frame
- openpyxl: to save to excel
- pycodestyle: to follow pep8 standard
- log4j: to manage the logs during the execution

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

📋 Deploy this project of Web Scrap with AWS

We could use AWS Elastic Beanstalk, which is a fully managed service that makes it easy to deploy, run, and scale web applications and services. 
Here are the steps:
- Create an AWS account if you don't already have one.
- Install the AWS Elastic Beanstalk Command Line Interface (CLI) on your local machine. This will allow you to interact with AWS Elastic Beanstalk from the command line.
- Create a new Elastic Beanstalk application and environment using the AWS Elastic Beanstalk CLI. This will create a new environment where you can deploy your web scraper.
- Pack your web scraper code and any dependencies into a zip file. This zip file will be uploaded to AWS Elastic Beanstalk as a deployment package.
- Use the AWS Elastic Beanstalk CLI to deploy your web scraper to the environment you created in step 3.
- Test your web scraper to ensure that it is running correctly on AWS Elastic Beanstalk.

Obs: Other options include using Amazon EC2, Amazon ECS, and Amazon EKS.

📄 Licence

- This project is under the license of Leonardo Rodrigues de Andrade

🤝 Support

Contributions, issues, and feature requests are welcome.
