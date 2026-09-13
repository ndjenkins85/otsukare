# Otsukare! Good work

Otsukare is a web application to help Japanese language students study.

This project was originally used in my masters degree for the 'Educational Technologies' subject. The subject had a lot of breadth, and I used this freedom to learn a new technology (the python flask framework).

The application is served at https://www.ndjenkins.com/projects/otsukare/.

* [Instructions for users](#instructions-for-users)
* [Instructions for developers](#instructions-for-developers)
  * [Dependency and virtual environment management, library development and build with poetry](#dependency-and-virtual-environment-management-library-development-and-build-with-poetry)
  * [Code quality, testing, and generating documentation with Nox](#code-quality-testing-and-generating-documentation-with-nox)
  * [Code formatting with Pre-commit](#code-formatting-with-pre-commit)
  * [Run local scripts](#run-local-scripts)
  * [Deploy to Railway](#deploy-to-railway)
* [Contributors](#contributors)

## Instructions for users

The following are the quick start instructions for using the project as an end-user.
[Instructions for developers](#instructions-for-developers) follows this section.

Visit [Otsukare on ndjenkins.com](https://www.ndjenkins.com/projects/otsukare/) to use the application.

## Instructions for developers

The following are the setup instructions for developers looking to improve this project.
For information on current contributors and guidelines see the [contributors](#contributors) section.
Follow each step here and ensure tests are working.

### Dependency and virtual environment management, library development and build with poetry

Use Python 3.12 and Poetry 2.1.1 or newer, along with poetry-version-plugin.

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

The application requires these environment variables and fails at startup if
`SECRET_KEY` or `DATABASE_URL` is absent:

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL connection URL (SQLite is supported for tests) |
| `SECRET_KEY` | High-entropy Flask session secret |
| `GATEWAY_AUTH_SECRET` | Must exactly match the identity helper's signing secret |
| `OTSUKARE_ADMIN_SUB` | Logto subject allowed to use administration features |
| `PORT` | Container listen port, supplied by Railway |

Run the local server after setting the variables with `poetry run python run.py`.
Requests other than `/healthz` must carry a valid gateway token for the exact
`/projects/otsukare` prefix.

The Logto cut-over intentionally discards all old users and their progress while
preserving core study content. It requires explicit confirmation:

```bash
poetry run python scripts/reset_users.py --yes
```

### Deploy to Railway

Build this repository's `Dockerfile`, set all variables above, and configure the
service health check as `/healthz`. The gateway must send
`X-Forwarded-Prefix: /projects/otsukare` and a signed `X-Gateway-Auth` header.


## Contributors

* [Nick Jenkins](https://www.nickjenkins.com.au) - Data Scientist, API & Web dev, Team lead, Writer

See [CONTRIBUTING.md](CONTRIBUTING.md) in Github repo for specific instructions on contributing to project.

Usage rights governed by [LICENSE](LICENSE)  in Github repo or page footer.
