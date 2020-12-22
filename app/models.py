'''
Models Module
~ all the stuff for SQL data storage
- There are 2+n tables:
    - Table 1: participants
        ~ contains info about each subject, the date they participated, and the experiments they went through
        - identified by the 'data_id' variable <-- if this gets linked to their "Name" (see Table 2), it is no longer anonymous
    - Table 2: names
        ~ subjects name, and whether they completed the experiment (for credit assignment)
    - Table `the rest`: experiment tables
        ~ each experiment gets it's own table, and it's used to track the condition assignment.
        - it will always be labelled in the format: 'experiment_<expname>'
'''
## python standard library
from datetime import datetime

## external 
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

## internal
from app import db, login
import config

## Participants Table (participant info; not direction tied to user identity unless you specify it to)
class Participant(UserMixin, db.Model):
    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), unique=False)
    status = db.Column(db.String(20), unique=False)
    experiments = db.Column(db.String(20), unique=False)
    temp_name_link = db.Column(db.String(20))
    condition = db.Column(db.String(20))

    ## add relations to all of the experiment tables
    # for exp in config.active:
        # names = db.relationship('experiment_' + exp, backref='participants', lazy='dynamic')

    def __repr__(self):
        return '<Participant {}>'.format(self.id)

@login.user_loader
def load_user(id):
    return Participant.query.get(int(id))



## Name Table (this contains participant identities)
class Name(UserMixin, db.Model):
    __tablename__ = 'names'

    id = db.Column(db.String(20), primary_key = True)
    name = db.Column(db.String(20), unique = False)
    status = db.Column(db.String(20), unique = False)

    data_id = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.id)


## Experiment Tables for Condition Tracking
experiment_tables = {}
for exp in config.experiments:
    experiment_tables[exp] = db.Table(
        'experiment_' + exp,
        db.Column('id', db.Integer, primary_key = True), 
        # db.Column('id', db.Integer, db.ForeignKey('participants.id')), 
        db.Column('condition', db.String(20)),
        db.Column('order', db.Integer), 
        # db.Column('data_id', db.Integer, db.ForeignKey('participants.id')),
    )

    # db.join(Participant, experiment_tables[exp])