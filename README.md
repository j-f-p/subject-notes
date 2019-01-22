# Subject Notes

## Description
This project is a web application for collaboratively posting notes about various topics about a subject. The app is developed with [Flask](http://flask.pocoo.org/) and employs [SQLAlchemy](https://www.sqlalchemy.org/) for managing its database. The demonstration database involves notes about [Deep Learning](https://en.wikipedia.org/wiki/Deep_learning). The application has user registration and authentication. Registered users are able to post, edit and delete notes. This was the second of four projects completed toward achieving the Udacity [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## Design
`newsdata.zip` contains information about news articles, authors of these articles and the history of internet requests to view the articles from a prior time period. `logsAnalysis.py` returns three tables of data processed from the database. The respective contents of the tables are:
<ul>
(Table 1) the most popular three articles from the database<br>
(Table 2) all the article authors listed in order of author article views<br>
(Table 3) the days on which more than 1% of article view requests failed
</ul>

The script is compatible with Python 3 and employs the psycopg2 Postgresql SQL database API. For each output table, there is a function for processing the data with SQL queries and a function for printing the results of the queries as a plain text table. In this way, the code is kept modular.

The SQL queries employ temporary views (they are not saved to the database) for reasons of convenience of human encoding and decoding. A couple of the views are employed to generate two of the output tables. Thus, they were created in a separate function. All of the SQL queries, including those for creating views, that are employed to generate the tables are listed below.

## Environment
The development environment for developing this project is a Linux virtual machine defined by the [Udacity FSND Virtual Machine][1] and provisioned by Vagrant 2.2.2 and VirtualBox 6.0. The web app was tested on Chrome, Firefox and Edge.

## Execution
* Install [Vagrant](https://www.vagrantup.com/)
* Install [VirtualBox](https://www.virtualbox.org/)
* Clone or download the [Udacity FSND Virtual Machine][1], which is contained by a repo head directory with various files and subdirectories.
* Give the repo head directory a relevant name and place it in an appropriate location. The repo `vagrant/` subdirectory contains files that are shareable between the host and guest operating systems, hereafter referred to as the vagrant directory.
* Enter the vagrant directory through a Linux command line interface. Then, install and boot the virtual machine by:
```bash
$ vagrant up
```
* Log into the virtual machine by:
```bash
$ vagrant ssh
```
* Clone or download this repo into a subdirectory of `vagrant/`.
* Enter that subdirectory and initialize the database by:
```bash
$ python database_setup.py
```
* Start the app server by:
```bash
$ ./subjectNotes.py
```
* Open one of the above modern browsers to `http://localhost:5000/subjectNotes`.

## Sample Output
Sample output is provided by `./output.txt`.

[1]: https://github.com/udacity/fullstack-nanodegree-vm
