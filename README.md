# AI3SW django-be
Django backend service for Fantacy Mentalwellness project

## Setup
### Clone the repository:

```sh
$ git clone https://github.com/AI3SW/django-be.git
$ cd django-be
```

### Python Environment Management using Conda

```bash
$ # create conda environment
$ conda env create --file environment.yml
$ conda activate django-mw
```

## Before Running
1. Setup database in desired destination

1. Update `ALLOWED_HOSTS` in [`settings.py`](mentalwellness/settings.py) with all possible IPs Django site can serve:

1. Update `DATABASES` in [`settings.py`](mentalwellness/settings.py) with target setting for all databases:

    * `'ENGINE': database backend to use`
    * `'NAME': The name of the database to use`
    * `'USER': The username to use when connecting to the database`
    * `'PASSWORD': The password to use when connecting to the database`
    * `'HOST': Which host to use when connecting to the database`
    * `'PORT': The port to use when connecting to the database`

1. Update `PREDICTION_MODEL_URL` in [`settings.py`](mentalwellness/settings.py) for AI models destination:

    * `'HOST': Which host to use when connecting to AI`
    * `'PORT': The port to use when connecting to AI`
    * `'ENDPOINT': The name of the endpoint to use`

1. Update `CONNECT_TO_DB` for input and output image database storage control

1. Create `media` directory in project folder

## Start Running

### Start Django server application

```sh
$ # To make your development server viewable to other machines on the network, use its own IP address (e.g. 10.2.119.9) or 0.0.0.0
$ python manage.py runserver 0.0.0.0:8000
```

You’ll see the following output on the command line:
```bash
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Django version 3.1.2, using settings 'mentalwellness.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C
```

Go to http://localhost:8000/ in your browser, and you should see the text `“Hello, this is index.”`

### Activating models

1. Create migration for styletransfer
    ```
    $ python manage.py makemigrations styletransfer

    Migrations for 'styletransfer':
    styletransfer/migrations/0001_initial.py

    $ python manage.py sqlmigrate styletransfer 0001

    BEGIN;
    --
    ...
    COMMIT;
    ```

1. Create migration for polls
    ```
    $ python manage.py makemigrations polls

    Migrations for 'polls':
    polls/migrations/0001_initial.py

    $ python manage.py sqlmigrate polls 0001

    BEGIN;
    --
    ...
    COMMIT;
    ```

1. Migrate models into database
    ```
    $ python manage.py migrate

    Operations to perform:
    Apply all migrations: admin, auth, contenttypes, polls, sessions, ...
    Running migrations:
    Rendering model states... DONE
    Applying styletransfer.0001_initial... OK
    Applying polls.0001_initial... OK
    ```

### Creating an admin user

Please fellow the instructions from this link: [creating-an-admin-user](https://docs.djangoproject.com/en/3.2/intro/tutorial02/#creating-an-admin-user)

## Additional Details

### django-be.styletransfer
* Application for Style Transfer model
* Instruction: [README.md](styletransfer/README.md)

### django-be.polls
* Application for questions and options poll
* Instruction: [ReadMe.md](polls/README.md)