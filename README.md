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

1. Update `ALLOWED_HOSTS` in [`settings.py`](mentalwellness/settings.py) with all host/domain names that this Django site can serve.
    * Please refer to link [here](https://docs.djangoproject.com/en/3.2/ref/settings/#allowed-hosts) 

1. Update `DATABASES` in [`settings.py`](mentalwellness/settings.py) with target setting for all databases:
    * Set your default database into `'default'` session
    * `'ENGINE'`: database backend to use
    * `'NAME'`: The name of the database to use
    * `'USER'`: The username to use when connecting to the database
    * `'PASSWORD'`: The password to use when connecting to the database
    * `'HOST'`: Which host to use when connecting to the database
    * `'PORT'`: The port to use when connecting to the database

1. Update `PREDICTION_MODEL_URL` in [`settings.py`](mentalwellness/settings.py) for AI models destination:

    * `'HOST'`: Which host to use when connecting to AI
    * `'PORT'`: The port to use when connecting to AI
    * `'ENDPOINT'`: The name of the endpoint to use

1. Update `CONNECT_TO_DB` for input and output image database storage control

1. Create `media` directory in project folder

## Start Running

### Start Django Server

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

### Activate models

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

### Create an admin user

Please follow the instructions here: [creating-an-admin-user](https://docs.djangoproject.com/en/3.2/intro/tutorial02/#creating-an-admin-user)

## Run Demo

Serveral demo pages are avaliable for different AI models
* [Stargan](http://127.0.0.1:8000/predict/stargan/demo)
* [Simswap](http://127.0.0.1:8000/predict/simswap/demo)

One page for all
* [All models](http://127.0.0.1:8000/predict/all/demo)

If you see an empty page when opening above link, you need to add styles before doing styletransfer
### Add styles into Database

1. visit django admin page [admin](http://127.0.0.1:8000/admin/) using admin account

1. Go to `Styletransfer -> Style Img`

1. Click `ADD STYLE IMG` on top right concer

1. Fill up all required field
    * `'File path'`: select and upload image from local directory
    * `'Model'`: Target AI model to support
    * `'Theme'`: Theme name for image
    * `'Is ref'`: Whether will be used as reference image
    * `'Ref class'`: class of reference image: `male` or `female`

1. Click `Save` and refresh demo page

## Additional Details

### django-be.styletransfer
* Application for Style Transfer model
* Instruction: [README.md](styletransfer/README.md)

### django-be.polls
* Application for questions and options poll
* Instruction: [ReadMe.md](polls/README.md)