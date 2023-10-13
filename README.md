Public Statements Interface (PS_Interface)
==========================================

PS_Interface is a Django based web application that serves as the interface to the public statements data pipeline. The pipeline is integrated separately from this web application in order to have a clear separation of concerns between the web application and the pipeline. While the pipeline function to scrape and process the data collected from the official's website, the web application uploads the processed data stored. 

_Note: As of the current version, the web application does not query the data stored by the pipeline, so a JSON model is shared between both the interface and the data pipeline. A JSON file a.k.a harvest file is uploaded onto the interface via the file_harvester page, which also serves as a manual backup in the event of a failed automatic querying from the interface to the pipeline's data._

<br>

## Requirements
- Python 3.10 or later
- pip version 22 or later
- Django package (already in requirements.txt)

<br>

## Installation
The installation process consists of a few parts, including the creation of a virtual environment to install the necessary python packages. 

#### Here is a breakdown:
1. Setting up virtual environment
2. Managing packages
3. Patching the source code (with secret files that are not included as part of version control)


### 1. Setting up virtual environment
-------------------------------------
Installing packages in a virtual environment is recommended. Python package 'virtualenv' is used in the development environment, though the application properly does not require using 'virtualenv'; any other virtual environment would do just fine.
### a. Install virtualenv

On Terminal (or any Unix shell):
```sh
pip install virtualenv
```

### b. Creating virtualenv (after installing virtualenv)

Virtual environment is stored in the user's home directory for convenience.

On Terminal (or any Unix shell):
```sh
mkdir -p ~/.virtualenvs
virtualenv ~/.virtualenvs/ps_interface
```

### c. Activating virtualenv

On Terminal (or any Unix shell):
```sh
source ~/.virtualenvs/ps_interface/bin/activate
```

<br>

### 2. Package management
-------------------------
This part will require you to change directory into the source code folder (ps_interface), and run a pip install command. (Make sure the virtual environment is activated before doing so)

After activating the virtual environment, within the source code directory, run the following command on Terminal (or any Unix shell):

```sh
pip install -r requirements.txt
```

The above command would install the dependencies that are required for the web application to function properly.


After the command had finished running, verify to see if the following packages have been installed:

```sh
Package            Version
------------------ ---------
...
Django             4.2.*
pg8000             1.30.*
ps-automation      1.0.*
...
```

The program may not work correctly if the above packages have not been installed.

<br>

### 3. Patching source code with files
--------------------------------------
The files will be send as a separate file due to it containing user credentials that is read-in by the web application. As such, are the SECRET_KEY to Django web application database and the connection info to the PVS database. I will note the examples of how these files will be structured. All of these files are ignored from the version control.

In the parent directory of the source code (where the requirements.txt and LICENSE reside), will contain the following files:

### connection_info.json
```json
{
    "host":"",
    "database": "",
    "port": 5432,
    "user": "",
    "password": ""
}
```

### .SECRETKEY
```
django-*blah blah(I am secret)
```

<br>

## Running the application

There is one more step to setup the application before running it:

1. Initialize web application database
2. Run
3. Managing & Maintenence (optional)


### 1. Initialize web application database
------------------------------------------
The web application database is automatically created by Django's makemigration command. This provide a way to store the necessary data that is displayed on the website, while also storing credentials of users. Read this [page](https://docs.djangoproject.com/en/4.2/topics/migrations) on [Django's documentation](https://www.djangoproject.com/) to learn more about migrations.

Within the source code directory, and on terminal (or any Unix shell):

```sh
python3 manage.py makemigrations
```

then,

```sh
python3 manage.py migrate
```

These commands initialize an empty database. The database stores information about the data in the harvest file that has been uploaded into VoteSmart's database.

<br>

### 2. Run
----------
After making migrations, the web application is ready to run. However, this step is skipped when hosting on a website.

### <span style="color:red">IMPORTANT!:<span>
### For deploying online, make sure to checkout this [documentation](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/).
<br>

#### To run it locally:
Within the source code directory, and on terminal (or any Unix shell):

```sh
python3 manage.py runserver
```

By default, the local hosting address would be http://127.0.0.1 with port number 8000.

```url
http://127.0.0.1:8000
```

<br>

### 3. Managing & Maintenence (optional)
----------------------------------------
The web application database may require some maintenance such as creation of new users, deletion of users, and altering uploaded information, etc. A superuser manages and handles these tasks. 

#### To create a superuser:
Follow the steps in this section of the [page](https://docs.djangoproject.com/en/4.2/topics/auth/default/#creating-superusers) in Django's documentation.


#### Accessing the admin of the website
While the application is running, you can type in the address followed by **'/admin'**, to administrate the tasks needed.
