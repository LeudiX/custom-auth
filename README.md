# Simple Student Inquiry Project with custom Auth User Model

For user authentication purposes using email and password credentials

## Installation

- Create your custom venv (py -m venv *venv-name*). You should always have one...
- Activate your venv (go to Scripts, inside your *venv-name* folder and activate the ven using *.\activate* cmd).You can also deactivate it using *deactivate* cmd  after work
- Go to your *venv* folder and install Django in it using (py -m pip install Django)
- Check Django version with (django-admin --version)
- Go to Base folder and create a new project *Only for 1st time project creation* with the cmd (django-admin startproject *project-name*)
- *Optional* Hide your secret key from settings.py in a env variable using (pip install django-environ)*See hide secret key reference for full guide on this operation* or check settings.py from line:23-29
- Run the server (py manage.py runserver)
- Create your app with (py manage.py startapp my_user_model)
- Register your app inside settings.py (INSTALLED_APPS)
