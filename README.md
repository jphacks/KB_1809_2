## How to use

Install Python 3.7.0 before development.
Recommend you to use macOS.

```bash
# OK
$ python -V
Python 3.7.0
# If your python is not 3.7.0
# On fish shell
$ set -x SSL_PREFIX (brew --prefix openssl)
$ env CFLAGS="-I$SSL_PREFIX/include" \
        LDFLAGS="-L$SSL_PREFIX/lib" \
        LD_RUN_PATH="$SSL_PREFIX/lib" \
        CPPFLAGS="-I$SSL_PREFIX/include" \
        CONFIGURE_OPTS="--with-openssl=$SSL_PREFIX" \
        pyenv install 3.7.0
# On bash shell
$ SSL_PREFIX=$(brew --prefix openssl)
$ CFLAGS="-I$SSL_PREFIX/include" \
        LDFLAGS="-L$SSL_PREFIX/lib" \
        LD_RUN_PATH="$SSL_PREFIX/lib" \
        CPPFLAGS="-I$SSL_PREFIX/include" \
        CONFIGURE_OPTS="--with-openssl=$SSL_PREFIX" \
        pyenv install 3.7.0
```

Clone repository and prepare environment.

```bash
$ ghq get https://github.com/jphacks/KB_1809_2
$ cd path/to/KB_1809_2
# Prepare dependencies
$ make deps
```

Here, you see '.venv' directory within `jphacks/KB_1809_2`.
You can open this repository in PyCharm.

### Start DB container

Prepare config

```bash
$ cp db.env.sample db.env
$ vim db.env
```

```bash
$ make rundb
# Stop
$ make stopdb
# Delete
$ make rmdb
```

### Prepare .env for app

```bash
$ cp api.env.sample api.env
$ vim api.env
```

### Migrate

```bash
$ pipenv run python manage.py makemigrations
$ pipenv run python manage.py migrate
```

Create super user

```bash
$ pipenv run python manage.py createsuperuser
```

Start server

```bash
$ pipenv run python manage.py runserver
```

### Build image

```bash
$ make image
```

## QA

`docker-compose.yml` is a QA environment. The structure of it is almost same as the production.

```bash
# Start
$ make qa-start
# Stop
$ make qa-stop
# Delete containers
$ make qa-clean
# Run manage.py in qa
$ make qa-manage ARGS="some command"
```