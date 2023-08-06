- [July 2023](#july-2023)
  - [25](#25)
  - [26](#26)
  - [27](#27)
  - [28](#28)
  - [30](#30)
  - [31](#31)
- [August](#august)
  - [01](#01)
  - [03](#03)
## July 2023
### 25
Objectives:
- Create trial Snowflake
- Familiarize with Snowpark and Python Snowflake connector
- [Configure Snowflake](https://www.youtube.com/watch?v=pZQXK7qO0iY)
    - Datawarehouse that's not COMPUTE_WH
    - Create roles and grant specific privileges to them
    - Create database within new data warehouse
    - Create schema within database
- Create table for storing sentiment data in Snowflake
- Figure out how I want to use the cloud
- Figure out what kind of data storage option I want to use
- Intro to Snowflake

Notes:
- [Potential good learning source for dbt](https://www.startdataengineering.com/post/dbt-data-build-tool-tutorial/)

Outcomes:
- Created trial account
- Watched half a video about [Snowpark](https://www.youtube.com/watch?v=udcFnIvXFnE)
- I will not use the cloud for now, I will only use Snowflake (which is still cloud but just not your standard cloud provider like AWS)
- The data storage option will be Snowflake
- Learned basics about Snowflake
- Used Snowpark to query my trial Snowflake Datawarehouse's sample database using the Python API for Snowpark https://docs.snowflake.com/en/developer-guide/snowpark/python/creating-session

### 26
Objectives:
- Deepen familiarity with Snowpark or Snowflake connector (functionionality)
- [Configure Snowflake](https://www.youtube.com/watch?v=pZQXK7qO0iY)
    - Datawarehouse that's not COMPUTE_WH
    - Create roles and grant specific privileges to them
    - Create database within new data warehouse
    - Create schema within database
- Create table for storing sentiment data in Snowflake
- Learn about DAC/RBAC
- Learn about [Snowflake architecture](https://www.youtube.com/watch?v=IocdgUB94KQ&list=PLba2xJ7yxHB7SWc4Sm-Sp3uGN74ulI4pS&index=4)
- Load raw data into Snowflake table
- Load historical data into Snowflake table

Notes:
- DAC - Objects not knowned by entities or individuals, rather by roles. When an entity or individual leaves/ gets deleted the objects do not get deleted. You can simply create another instance of that role and assign it to an individual and they will now also be owners of those objects as they belong to said role.

Outcomes:
- Successfully configured Snowflake today. Created a developer role with enhanced privileges and created relevant database, schema, and table.
- Successfully loaded raw data into Snowflake table using Snowpark for today and then also historical data up to 90 days back.
- Need to look into utilizing DBT for transformations now and creating separate schemas for raw and transformed data. Might look into using Python for transformations as a start then switch to DBT.
- Need to standardize code and remove hard coded values as well.
- Did some extra! Created DBT cloud trial account and connected it to my Snowflake account. Also connected DBT to my git repository and instantiated a DBT project in the repo!

### 27
Objectives:
- Finish DBT fundamentals course and become familiar with core DBT concepts
- Integrate DBT into my project. Perhaps just use it to perform a simple transformation of my data in Snowflake and publish a model? if that's how the terminology goes

Notes:
- Models are just SQL files which represnt logic that transforms raw data into transformed data. They "model" your data. Each model maps 1:1 with a table or view in the data warehouse (general rule, has a few exceptions)
- DBT will handle DDL/DML you don't need to handle it. I focus on just transformations, don't need to worry about dependencies and DDL/DML.

Outcomes:
- Watched a few more videos on the models section of the course, enough for me to do the rest of the tasks
- Integrated DBT into my project. Created a new model for stg_news_sentiment which captures cleaned and semi-transformed data to be used

Notes:
- Very much a tool we could have used to DWBT, very interesting.

### 28
Objectives:
- Watch rest of DBT fundamentals course videos, or relevant ones to find out what I want to do next
- Implement modularity into DBT
- Pull more data sources in?

### 30
Objectives:
- Same as on the 28th
- Tidying up roles and refresher on RBAC. My one developer role got messy because I didn't build a hierarchy. Need to fix this. (https://www.analytics.today/blog/snowflake-system-defined-roles-best-practice)
-  Create USERADMIN role to provision roles and create users
-  Create DEVELOPER role which can create warehouses and databases something which the USERADMIN cannot do
-  Create a developer user and assign it the developer role
-  DBT core vs DBT cloud

Outcomes:
- Set up roles correctly and provisioned them as per best practice:
  - ACCOUNTADMIN usage limited
  - USERADMIN for provisioning roles and users
  - SYSADMIN for granting warehouse, and database privileges
  - custom DEVELOPER role to be granted the ability to create databases and create objects within it
  - SYSADMIN to inherit DEVELOPER role
  - Completed literally everything I wanted to. Very clean RBAC implemented. "DEVELOPER" role will be the creator of all database objects.
    - All configuration ran through this new role in the script
    - DBT cloud re-configured to use new role and new objects owned by the role
    - Re-imported raw data successfully, model in DBT for stg_news_sentiment also ran successfully.
    - EVERYTHNG IS A GOOOO! Big success today

### 31
Objectives:
- Watch the rest of the DBT fundamentals course
- Write out in simple terms what RBAC is, and what the best practice is in Snowflake
- Re-structure current "stg_news_sentiment" as per best practice
  - https://github.com/dbt-labs/corp/blob/main/dbt_style_guide.md
- Update elt.py script to dynamically call write_pandas to upsert into RAW table
- Import some other data sources from AlphaVantage
  - Explore AV to see what other data interests me and pull that
- Learn about [Snowflake architecture](https://www.youtube.com/watch?v=IocdgUB94KQ&list=PLba2xJ7yxHB7SWc4Sm-Sp3uGN74ulI4pS&index=4)

Notes:
- Role based access control is a method of provisioning access, or a way in which part of data governance is enforced by restricting access to "roles" rather than individual users. Roles can be pre-determined or custom created. In the context of Snowflake, there are some default roles such as USERADMIN and SYSADMIN which can be assigned at the beginning but you can and should create your own roles to provision differing levels of access depending on the role and users will be assigned roles depending on which team and therefore what level of access to the Snowflake account they will have. For example, analysts will not need to create warehouses or databases therefore their role will not have these privileges whereas a project manager role will.

Outcomes:
- Finished "Models" section of DBT fundamentals course
- stg_news_sentiment already created as per most best practices I believe.
- Updated elt.py script to add some logging and function to upsert raw data to Snowflake. Still needs some work.

## August
### 01
Objectives:
- Gain an understanding of the concept of marts and stage as per best practice from dbt
- [Implement the "ref" functionality from dbt into my project with stage and mart models ](https://www.getdbt.com/analytics-engineering/modular-data-modeling-technique/)
- Finish updating elt.py to reduce redundancy
- Watch the "Sources" section of the dbt fundamentals course
- Implement sources into dbt project
- Familiarize with tests in dbt
- Work out how all the yml files work with each other and how they're different from each other as well as best practices

Notes:
- Staging and mart model categories are a way to modularize data modelling. Staging models will contain raw data that has been prepared, for example simple clean ups and transformation on raw data for things like making the date columns correct, converting "n/a" strings into nulls, etc.
- Marts is where you start to apply business logics and therefore will usually contain heavier transformations. Mart models will reflect core business data assets that will be used directly for analytics. Marts will contain your fact and dim tables. Think of it as the "DB_LOAD" schema in DWBT.
  - The Mart layer will often contain tables that utilize multiple staging models and use joins, case whens, window functions, etc. the more complex transformations.
- Note there are more layers such as base, and intermediate but these are usually for more complex data models and I will not be using them in my project.
- dbt build combines dbt test and dbt run
- Best practice for yml file structure is to have cascading configs, taking advantage of the organized structure of your project. Have a __models in each end sub-directory to configure that sub-directorie's models. For example, in marts/finance there will be a finance__models.yml file which will configure the models in the finance mart. Also __sources.yml will be present in the staging models. For exmaple in staging/jaffle_shop model category there will be a _jaffle_shop_sources.yml to define the raw data sources for jaffle shop staging models.

Outcomes:
- Gained understanding of when to use stage and marts as model concepts in dbt
- Completed "Sources" section of fundamentals course
- Successfully implemented sources into dbt project

### 03
Objectives:
- Explore Snowpark more, gain a deeper understanding and become more proficient at using it
- Ingest another data source, create another source table in Snowflake
- Implement some tests into dbt project
- Have a quick look into Terraform

Notes:
[Some amazing reads on how Gitlab structures their data platform](https://gitlab.com/gitlab-data/analytics/-/blob/master/transform/snowflake-dbt/models/overview.md)

Outcomes:
- Didn't get much done. Haven't touched the project since this day, needed a little break.