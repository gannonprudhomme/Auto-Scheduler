# Auto-Scheduler
## Install
1) First you need to need to install python
2) Second, you'll need to install Django. Do this by running `pip install Django`
3) Third, you'll need to install Postgresql, which is our database of choice. Run `pip install psycopg2` to do so.
4) You might need to install Postgresql from someplace else but honestly I'm not sure, it differed widely from when I did it on Windows 10 vs macOS
5) Once you have PostgresQL installed, you'll need to create the `dbautoscheduler` database
    a) You can do this by opening the PostgresQl command line(type `psql` in command line) then type `CREATE DATABASE dbautoscheduler;`