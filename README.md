Public Statements Interface (ps_interface)
==========================================

About
-----
ps_interface is a Django based web application that serves as the interface to the Vote Smart's public statements data pipeline. The pipeline is integrated separately from this web application in order to have a clear separation of concerns between the web application and the pipeline. While the pipeline functions to scrape and process the data collected from political incumbents' websites, the web application uploads the processed data from the pipeline. 

_Note: As of the current version, the web application does not query the data stored by the pipeline, so a JSON model is shared between both the interface and the data pipeline. A JSON file a.k.a harvest file is uploaded onto the interface via the file_harvester page, which also serves as a manual backup in the event of a failed automatic querying from the interface to the pipeline's data._

<br>

## Requirements
- Python 3.10 or later
- pip version 22 or later
- Django package (already in requirements.txt)

<br>


## Getting Started
In this section,  you will find the steps to initialize the application and to make sure that it runs as intended.


### 1. Package Installation
---------------------------
The application is developed on Django 4.2+, therefore Django >4.2 is the main dependency. There are a few other external dependencies eg. Pillow, psycopg and python-decouple.


Within the project directory, and on terminal (or any Unix shell), type:

```sh
pip install -r requirements.txt
```

<br>

### 2. Environment file
-----------------------
There are variables that are not uploaded onto the repo, such as the SECRET key and  database connection info. This application references a local environment file to store these variables. The production stage should follow suit with the development stage.

Within the project directory, should contain the following file:

### .env

The .env file contains variables such as the SECRETKEY and connection info to the VoteSmart's database. [python-decouple](https://pypi.org/project/python-decouple/) package is used to read the variables in the .env file. On the repo, the env.sample file sets the template for creation of the .env file.

ps_interface stores application data on a postgres database. Look on Django's documentation to learn more about how [to work with postgres on Django](https://docs.djangoproject.com/en/4.2/ref/databases/#postgresql-connection-settings).

<br>


### 3. Initialize application's database
----------------------------------------
The application database can be created by Django's built-in commands. This provide a way to store the application data and user credentials.

Within the project directory, and on terminal (or any Unix shell), type:

```sh
python3 manage.py makemigrations
```

then,

```sh
python3 manage.py migrate
```

Once the initial migrations are made, create the following files and place them into their individual respective folders:

#### add_harvest_status.py ({*_project directory_*} -> ps_harvester -> migrations)

```python
def initiate_status(apps, schema_editor):

    harvest_status = apps.get_model('ps_harvester', 'HarvestStatus')
    
    initial_status = [
        (1, 'COMPLETE'),
        (2, 'INCOMPLETE'),
        (3, 'PENDING REVIEW'),
        (4, 'ERROR')
    ]
    
    for status_id, status_name in initial_status:
        harvest_status.objects.create(status_id=status_id, status_name=status_name)


class Migration(migrations.Migration):

    dependencies = [
        ('ps_harvester','0001_initial')
    ]

    operations = [
        migrations.RunPython(initiate_status)
    ]
```
The above Python code creates the table rows required for associating a harvest process with a status.

Look on Django's documentation to learn more about [Django's database migrations](https://docs.djangoproject.com/en/4.2/topics/migrations).

<br>


### 4. Configuring Static Files
-------------------------------
Some hosting platforms requires a configuration of the static files.

Here are the links to the static files:

#### *{project_directory}*/static
#### *{project_directory}*/ps_auth/static
#### *{project_directory}*/ps_harvester/static
#### *{project_directory}*/ps_user/static

<br>

### 5. Administration
---------------------
The web application can create, delete and authenticate users. Each user will be assign to a user group with the exception of the superuser. The following are the user groups:

1. Director
2. Staff
3. Intern

 A superuser manages the initial verification and deletion of users, along with the task of handling all the data within the application. Further verification and user management will be handled by the Director user group. 

#### To create a superuser:
Follow the steps in this section of the [page](https://docs.djangoproject.com/en/4.2/topics/auth/default/#creating-superusers) in Django's documentation.

#### Accessing the admin of the website
As a superuser, you can type in the url path **'/admin'**, to administrate and manage users and the application data.