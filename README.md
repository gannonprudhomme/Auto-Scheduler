# Auto-Scheduler
## Install
Follow these steps to start a local Django server using a PostgreSQL database:
1) If you don’t have it already, download Python from [here](https://www.python.org/downloads/).
2) The app runs within a virtualenv called "django_app". Before you activate the venv and install the requirements make sure you have postgres setup correctly

```
MacOS (there is a known bug with psycopg2 on mac);

brew install postgres 
Add postgres executable to your PATH (ie open up ~/.bash_profile and append /usr/local/bin/postgres to your PATH)
brew reinstall openssl
export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/

Ubuntu;
sudo apt-get install libpq-dev python-dev
sudo apt-get install python3-Psycopg2
sudo apt-get install python3-pip

```
Then you can activate your env and install the requirements; 
```
source django_app/bin/activate
pip3 install -r requirements.txt

```
Now to run the app, make sure to source your venv before running. Your global python env does not include the deps in requirements.txt anymore, only the venv does. A good way to see the different is to run pip3 list before and after activating the venv.

You may also want to download pgAdmin 4 for ease of database management (it can be installed with PostgreSQL if you used the about Windows/Mac guide). It can also be downloaded from [here](https://www.pgadmin.org/download/).
4) (Only if using pgAdmin) Create a new server by opening pgAdmin and right-click “Servers->Create->Server…”. Set a name pgAdmin will use (it can be anything), then change to the Connection tab. Ensure the following settings are being used:  
Host name/address: localhost  
Port: 5432  
Maintenance database: postgres  
Username: postgres  
Password: (not necessary)  
5) Ensure the database `dbautoscheduler` has been created:  
Using psql: Type `\l` in the psql prompt and see if `dbautoscheduler` is in the list.  
Using pgAdmin: Click the name of the server you created, and see if `dbautoscheduler` is in the tree menu.
6) If you'd like to get the current project running, you can clone the repository with `git clone https://github.com/gannonprudhomme/AutoScheduler/` and run the steps below.

## Running
The only thing set up currently is scraping a single department worth of courses(CSCE) and scraping all of the departments.

To do these,

1) Run `cd autoscheduler`
2) Run `./manage.py makemigrations` and `./manage.py migrate` to generate SQL that will be used to fill the database.
3) Run `./manage.py createsuperuser` to create a user for Django.
3) Run `./manage.py scrape_dept` to scrape all of the available departments.
4) Run `./manage.py scrape_courses` to scrape the courses, sections, and instructors.

If `./manage.py` isn't working, try to use `python manage.py` or `python3 manage.py` in place of it. 
