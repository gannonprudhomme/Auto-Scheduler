# Auto-Scheduler
## Install
Follow these steps to start a local Django server using a PostgreSQL database:
1) If you don’t have it already, download Python from [here](https://www.python.org/downloads/).
2) Run the following in your command line interface to install the python packages necessary to run our database and server:
```
pip install Django
pip install psycopg2
```
3) Set up a PostgresQL server by following one of these guides, and make sure you set the name of the database when prompted to `dbautoscheduler`:  
[Windows/Mac](http://www.postgresqltutorial.com/install-postgresql/)  
[Linux](https://www.techrepublic.com/blog/diy-it-guy/diy-a-postgresql-database-server-setup-anyone-can-handle/)  
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

## Running
The only thing set up currently is scraping a single department worth of courses(CSCE) and scraping all of the departments.

To do these,

1) Run `cd autoscheduler`
2) Run `./manage.py scrape_depst` to scrape all of the available departments.
3) Run `./manage.py scrape_courses` to scrape the courses, sections, and instructors.
