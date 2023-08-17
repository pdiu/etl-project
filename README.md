# ETL Project
Personal ETL project utilizing core modern technologies to expand/refresh my data engineering skills.

Please find the deployed visualizations app at https://lph-etl-project.streamlit.app/

These skills are:
- Using Python to make API calls to retrieve data (**E**LT)
- Python for loading data into data store (E**L**T)
- Snowflake as the data warehouse platform
  - Using Snowflake efficiently from an administration POV. This means implementing best practice RBAC.
- Prefect for task orchestration
- DBT for analytical engineering, particularly with data transformations (EL**T**)
- Azure/AWs for hosting a virtual machine, and therefore AWS/Azure SDK for IaC
- Docker container running on cloud VM
- Streamlit for creating a web application for interactive exploration of the data and data visualizations

# Notes
## Virtual environment
A virtual environment is used which is not tracked by git as per best practice. You can find all libraries required for this project in requirements.txt. To install all of them simply call ```pip install -r requirements.txt```

## Config data
This repository tracks configuration which is not shared. You can create your own configs within them.
- *secrets.json* contains API keys
- *snowflake.json* contains Snowflake credentials

## Other    
I will be implementing best practices along the way. This includes but is not limited to
- Proper logging with the built-in Python module *logging*
- Proper usage of configuration files
- Proper usage of virtual environments
- Proper usage of version control practices