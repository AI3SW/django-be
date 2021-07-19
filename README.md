# AI3SW django-be
Django backend service for Fantacy Mentalwellness project

## Python Environment Management using Conda

```bash
$ # create conda environment
$ conda env create --file environment.yml
$ conda activate django-mw
```
## Before Running
1. Setup correct database in desired location:

1. Update `ALLOWED_HOSTS` in [`settings.py`](mentalwellness/settings.py) with all possible IPs Django site can serve:

1. Update `DATABASES` in [`settings.py`](mentalwellness/settings.py) with target setting for all databases
        * 'ENGINE': database backend to use

        * 'NAME': The name of the database to use

        * 'USER': The username to use when connecting to the database

        * 'PASSWORD': The password to use when connecting to the database

        * 'HOST': Which host to use when connecting to the database

        * 'PORT': The port to use when connecting to the database

1. Create `media` directory in project folder

1. Create `logs` directory in project folder for storage of log files
ss

## Start Running

## Introduction for components

### django-be.styletransfer
* Application for Style Transfer model
* Instruction: [README.md](styletransfer/README.md)

### django-be.polls
* Application for questions and options poll
* Instruction: [ReadMe.md](polls/README.md)