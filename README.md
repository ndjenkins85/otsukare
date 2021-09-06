# Otsukare! Good work

Otsukare is a web application to help Japanese language students study.

This project was originally used in my masters degree for the 'Educational Technologies' subject. The subject had a lot of breadth, and I used this freedom to learn a new technology (the python flask framework).

The alpha version website is online at https://otsukare.herokuapp.com/

* [Instructions for users](#instructions-for-users)
* [Instructions for developers](#instructions-for-developers)
  * [Dependency and virtual environment management, library development and build with poetry](#dependency-and-virtual-environment-management-library-development-and-build-with-poetry)
  * [Dependency and virtual environment management, library development and build with conda](#dependency-and-virtual-environment-management-library-development-and-build-with-conda)
  * [Code quality, testing, and generating documentation with Nox](#code-quality-testing-and-generating-documentation-with-nox)
  * [Code formatting with Pre-commit](#code-formatting-with-pre-commit)
  * [Run local scripts](#run-local-scripts)
  * [Deploy to Heroku](#deploy-to-heroku)
* [Contributors](#contributors)

## Instructions for users

The following are the quick start instructions for using the project as an end-user.
[Instructions for developers](#instructions-for-developers) follows this section.

Visit the [heroku website](https://otsukare.herokuapp.com/) to use the application.

## Instructions for developers

The following are the setup instructions for developers looking to improve this project.
For information on current contributors and guidelines see the [contributors](#contributors) section.
Follow each step here and ensure tests are working.

### Dependency and virtual environment management, library development and build with poetry

Ensure you have and installation of Poetry 1.2.0a1 or above, along with poetry-version-plugin.

Make sure you deactivate any existing virtual environments (i.e. conda).

```bash
poetry install
```

You may need to point poetry to the correct python interpreter using the following command.
In another terminal and in conda, run `which python`.
```bash
poetry env use /path/to/python3
```

Library can be built using

```bash
poetry build
```

### Dependency and virtual environment management, library development and build with conda

Following commands will create the conda environment and setup the library in interactive development mode using setup.py.

```bash
conda env create -f environment.yml
conda activate my_project
pip install -e .
```

Library can be built using

```bash
python setup.py bdist_wheel
```

### Code quality, testing, and generating documentation with Nox

Nox is a python task automation tool similar to Tox, Makefiles or scripts.

The following command can be used to run mypy, lint, and tests.
It is recommended to run these before pushing code, as this is run with Github Actions.
Some checks such as black are run more frequently with [pre-commit](#code-formatting-with-pre-commit).

```bash
poetry run nox
```

Local Sphinx documentation can be generated with the following command.
Documentation publishing using Github Actions to Github pages is enabled by default.

```bash
poetry run nox -s docs
```

All other task automations commands can be optionally run locally with below command.

```bash
poetry run nox -s black safety pytype typeguard coverage xdoctest autoflake
```

### Code formatting with Pre-commit

On first time use of the repository, pre-commit will need to be installed locally.
You can use the following command to install and run pre-commit over all files.
See .pre-commit-config.yaml for checks in use.
Intention is to have lightweight checks that automatically make code changes.

``` bash
pre-commit run --all-files
```

### Run local scripts

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
python run.py
```

6. Visit local website http://localhost:5000/


### Deploy to Heroku

Once updates have been made to the scripts, can redeploy the web service on Heroku using the following. This should be done when ready to deploy after a git master branch update.
``` bash
git push heroku master
```

Read logs to determine if deployment was successful. Following are some useful commands to verify;

``` bash
heroku open
heroku logs --tail
```


## Contributors

* [Nick Jenkins](https://www.nickjenkins.com.au) - Data Scientist, API & Web dev, Team lead, Writer

See [CONTRIBUTING.md](CONTRIBUTING.md) in Github repo for specific instructions on contributing to project.

Usage rights governed by [LICENSE](LICENSE)  in Github repo or page footer.
