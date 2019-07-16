Biflorica's Data Collector
==========================

Prerequisites
-------------

If you try to run it bear in mind that you'll need:

* A working install of postgresql and have to specify the username and 
password in config.ini. 
* Package libpq-dev installed (in Ubuntu/Debian systems)

Install
-------

I recommend you to install as `develop` inside a python virtual environment. 

```
$ mkdir /path/to/folder
$ mv biflorica.tar.gz /path/to/folder
$ cd /path/to/folder
$ tar xvf biflorica.tar.gz
$ virtualenv env/
$ source env/bin/activate
```

Before next step, make sure everything in config.ini is correctly set as
this instruction will read and write data to this file.

```
$ python setup.py develop
```

That will create two executables:

* setup: creates the tables inside the database and populates it with
the basic stuff needed to start collecting data, including: farms, types of
flowers, varieties of flowers, sizes, etc. Everything is pulled down from
biflorica and stored in your database.
* record: this is the collector itself. When executed, it starts
fetching trading data indefinitely from biflorica (starting with the most
current bid/offer and going back in time) until we collide and reach to
the latest data recorded in the database. It has to be done this way since the
API does not have the option to fetch specific id's or timestamps, only
bulks of rows.
