import os
basedir = os.path.abspath(os.path.dirname(__file__))

host = '0.0.0.0' # <-- this is the base URL you're running from
port = 8001 # <-- this is the port you want to send traffic through. To open up this port, you'll likely have to ask your university's Information Technology Services team

SECRET_KEY = 'this is a secret key code' # <-- this is how (i think) flask keeps track of user session data; if it changes, all sesion data is lost on restart. probably best not to regenerate it everytime (though that's what i do for the `temp_name_link` *shrug*)
    # ^ you can make a new one with: os.urandom(32)
path_to_participants_db = 'sqlite:///' + os.path.join(basedir, 'data/database.db')
    # ^ you really dont have to mess with this if you want to stick with sqlite. experiment data will be stored as normal files, so you don't *necessarily* need to learn SQL to use the webrunner

security = 'confidential' # options: 'confidential', 'anonymous'
# security = 'anonymous' # options: 'confidential', 'anonymous'

show_exit_survey = False

SONA = True
SONA_link = 'link to your sona completion url (see experiment manual)'


## experiment config (do **not** start your experiment name with an underscore _ [to prevent conflict with default pages])
experiments = {
    'oCanvas_example': {
        'template': 'oCanvas_example.html', # <-- this file _has to be unique_, do not use a name that overlaps with another template (feel free to throw it in it's own folder)
        'data': 'oCanvas_example', # <-- folder where you want the data to be stored
        'conditions': ['1','2'], # <-- these will be automatically assigned by the webrunner
    },
    'jsPsych_example': {
        'template': 'jsPsych_example.html',
        'data': 'jsPsych_example',
        'conditions': ['one','two'],
    },
}

active = [
    'oCanvas_example',
    'jsPsych_example',
]

