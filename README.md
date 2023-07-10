# ETL Project
Personal ETL project utilizing core modern technologies that I want to learn to expand my data engineering skills.

These technologies are:
- API familiarization. Using Python to make API calls to retrieve data (**E**LT)
- Python for loading data into data store (E**L**T)
- Prefect for task orchestration
- dbt for analytical engineering, particularly with data transformations in the EL**T** process
- Streamlit for creating a web application for interactive exploration of the data and data visualizations
- Cloud interwoven into ll these aspects

# Notes
## Virtual environment
A virtual environment is used which is not tracked by git as per best practice. You can find all libraries required for this project in requirements.txt. To install all of them simply call ```pip install -r requirements.txt```

## Config data
This repository does not track my personal config file which the elt.py script will refer to as "secrets.json".

## Other
I will be implementing best practices along the way. This includes but is not limited to
- Proper logging with the built-in Python module *logging*
- Proper usage of configuration files
- Proper usage of virtual environments
- Proper usage of version control practices