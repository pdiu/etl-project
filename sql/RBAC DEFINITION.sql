-- Run user and role object related tasks from USER_ADMIN role
CREATE USER LPH_SYSADMIN PASSWORD = "*****" DEFAULT_ROLE = "SYSADMIN";
CREATE USER LPH_DEV PASSWORD = "*****" COMMENT = "This is the all powerful developer user";
CREATE USER LPH_READ_ONLY PASSWORD = "*****" COMMENT = "This is for analyst users, where only read only access is required"

CREATE ROLE DEVELOPER;
CREATE ROLE ACCESS;

-- Set up privilege hierarchy
GRANT ROLE ACCESS TO ROLE DEVELOPER;
GRANT ROLE DEVELOPER TO ROLE SYSADMIN;
GRANT ROLE ACCESS TO USER LPH_READ_ONLY;

-- Provision roles to users
GRANT ROLE DEVELOPER TO USER LPH_DEV;
GRANT ROLE SYSADMIN TO USER LPH_SYSADMIN;

-- Use SYSADMIN here as USER_ADMIN cannot grant privileges on the database and warehouse level
GRANT CREATE WAREHOUSE ON ACCOUNT TO ROLE "DEVELOPER";
GRANT CREATE DATABASE ON ACCOUNT TO ROLE "DEVELOPER";
GRANT USAGE ON WAREHOUSE TRANSFORMER TO ROLE "ACCESS";
GRANT USAGE ON DATABASE MARTS TO ROLE "ACCESS";
GRANT READ ON DATABASE MARTS TO ROLE "ACCESS";