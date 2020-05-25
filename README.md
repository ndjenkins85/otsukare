# Otsukare! Good work

A proof of concept website to help users learn Japanese.

This project was originally used in my masters degree for the 'Educational Technologies' subject. The subject had a lot of breadth, and I used this freedom to learn a new technology (the python flask framework).

The website is still online (although buggy) at https://otsukare.herokuapp.com/

*Always interesting to go back to old code to reflect on how far one has come. It's so obvious to me now how important a README.md file is, and it sucks that I didn't provide any getting started information!*

## Getting started

Guide to running the scripts locally.

1. Project uses Pipenv. I have updated the 'Pipfile' to use python 3.7 and fixed a dependency

``` bash
pip install pipenv
pipenv install
```

2. Local postgres instance required https://postgresapp.com/downloads.html

3. Create otsukare database

``` bash
/Applications/Postgres.app/Contents/Versions/12/bin/psql -c "create database otsukare"
```

4. Populate postgres:otsukare database

``` bash
pipenv shell
python manage.py create_db
python manage.py add_db
```

5. Run otsukare webserver (from within pipenv shell)
``` bash
python otsukare.py
```

6. Visit local website http://localhost:5000/


# TODO List

- [] Scrub secrets found in manage.py
- [] Delete unneeded files, cleanup directories


