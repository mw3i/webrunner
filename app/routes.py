# python standard lib 
import json, os, uuid

# external resources
from flask import Flask, redirect, url_for, request, render_template, make_response, jsonify,send_from_directory, flash
from flask_login import current_user, login_user, logout_user, login_required, login_manager
from flask_sqlalchemy import SQLAlchemy

# internal resources
from app import app, db, ops, forms
from app.models import Participant, Name
import config


# - - - - - - - - - - - - - -
#      Default Pages
# - - - - - - - - - - - - - -
@app.route('/', methods = ['GET', 'POST'])

def main():
    if request.user_agent.platform in ['iphone', 'android']:
        return render_template('errors/_mobileRedirect_.html')

    form = forms.ConsentForm()
    if form.validate():
        participant, name = ops.new_user(form.name.data)
        ops.save_consent_form(name.name)
        exp, condition = ops.get_next_experiment_condition(participant)
        participant.condition = condition
        db.session.commit()
        login_user(participant)
        
        first_exp = json.loads(participant.experiments)[int(participant.status)]
        return redirect(url_for('load_exp', exp = first_exp))

    return render_template('_startpage_.html', form = form)


# Exit Survey & Debriefing Page
@app.route("/_exit_", methods = ['GET', 'POST'])
# @login_required
def exit_page():
    form = forms.DebriefForm()
    if form.validate():
        misc_id = uuid.uuid4()
        while str(misc_id)+'.txt' in os.listdir('data/_exitsurveys_/'):
            misc_id = uuid.uuid4()
        with open(os.path.join('data/_exitsurveys_/', str(misc_id)+'.txt'), 'w') as file:
            for field in form:
                if field.id != 'csrf_token':
                    print(field, file = file)
            return redirect(url_for('finalmessage_page'))

    return render_template('_exitpage_.html', form = form, show_exit_survey = config.show_exit_survey)


# If they choose to exit
@app.route("/_noconsent_exit_")
def noconsent_exit():
    return render_template('_noconsent_exit_.html')


# Final Message
@app.route("/_finalmessage_")
# @login_required
def finalmessage_page():
    logout_user()
    if config.SONA == True:
        return render_template('_finalmessage_.html', assign_SONA_credit = True, SONA_link = config.SONA_link)
    else:
        return render_template('_finalmessage_.html')


# Cheater Message (if automatic credit assignment didn't work)
@app.route("/_crediterror_")
def creditassignerror_page():
    return render_template('errors/_creditassignerror_.html')


@app.route("/_misc_err_")
def misc_err_page():
    return render_template('errors/_misc_err_.html')


@app.route("/_iei_")
def transition_page():
    return render_template('_transitionpage_.html', instructions = 'Hey')



# - - - - - - - - - - - - - -
#      Experiment Pages (dynamically add routes based on experiments in the config file)
# - - - - - - - - - - - - - -
# from: http://www.compjour.org/lessons/flask-single-page/multiple-dynamic-routes-in-flask/
@app.route('/<exp>')
# @login_required
def load_exp(exp):
    if exp in config.active:
        return render_template(os.path.join('experiments/', config.experiments[exp]['template']))
    else:
        return render_template('errors/404.html')



# - - - - - - - - - - - - - -
#      Operations (routes that lead to some server action being done)
# - - - - - - - - - - - - - -
@app.route('/_next_', methods=['POST'])
# @login_required
def next():
    message = request.get_json()

    if current_user.is_authenticated == False:
        return make_response(
            json.dumps({
                'next_page': '/_misc_err_',
            })
        )        

    if current_user.status == 'finished':
        return make_response(
            json.dumps({
                'next_page': '/_finalmessage_',
            })
        )

    else:
        ## save subject data
        current_exp = json.loads(current_user.experiments)[int(current_user.status)]
        ops.save_subject_data(
            os.path.join('data/experiments', config.experiments[current_exp]['data'], str(current_user.id)), 
            message,
        )

        ## update databases
        current_user.status = int(current_user.status) + 1
        name = db.session.query(Name).filter_by(
            id = ops.decrypt_name(current_user.temp_name_link)
        ).first()
        name.status = current_user.status

        ## get next exp to run
        if int(current_user.status) >= len(json.loads(current_user.experiments)):
            current_user.status = 'finished'
            name.status = current_user.status
            current_user.condition = '_done_' 
            next_page = '/_exit_'
        else:
            exp, condition = ops.get_next_experiment_condition(current_user)
            current_user.condition = condition 
            next_page = '/_iei_?next_exp=' + exp

        db.session.commit() # <-- commit changes to db

        return make_response(
            json.dumps({
                'next_page': next_page,
            })
        )        

