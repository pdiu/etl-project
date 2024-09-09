# ETL Project
Personal ETL project utilizing core modern technologies to expand/refresh my data engineering skills.

Please find the deployed visualizations app at https://lph-etl-project.streamlit.app/

These skills are:
- Using Python to make API calls to retrieve data (**E**LT)
- Pandas for loading data into data platform (E**L**T)
- Snowflake as the data warehouse platform
  - Using Snowflake efficiently from an administration POV. This means implementing best practice RBAC
- Airflow for task orchestration
- DBT for data modelling and transformation under software engineering frameworks (EL**T**)
- Docker container for running everything, also so that anyone can run it from anywhere as long as they clone this repo and follow the instructions
- Streamlit for creating a web application for interactive exploration of the data and building data visualizations

# Setup
## 1.Virtual environment
Create a virtual python virtual environment in the root directory of this project ```python -m venv venv``` followed by ```source venv/bin/activate``` to activate the environment

All Python dependencies are tracked in requirements.txt file. With your virtual env activated run this command  ```pip install -r requirements.txt```

## 2.Config data
You will need to create a .env file to store your config which will be stored as environment variables when running the setup.py script. There is a template called .env_template which you can copy and rename to .env after filling in the values.

# Notes    
I will be implementing best practices along the way. This includes but is not limited to
- Proper logging with the built-in Python module *logging*
- Proper usage of configuration files
- Proper usage of virtual environments