# python standard lib 
import json, copy, random, uuid, datetime

# external

# internal
from app import app, db, encryptor
from app.models import Participant, Name, experiment_tables
from sqlalchemy import func, insert 
import config


def new_user(participant_name):
    name_id = get_name_id()
    name_encoded = encryptor.encrypt(name_id.encode())

    ## Make new user
    data_id = get_last_data_id() + 1
    participant = Participant(id = data_id, date = get_formatted_date(), status = 0, experiments = get_experiment_order(), temp_name_link = name_encoded)
    db.session.add(participant)
    db.session.commit()

    linked_data_id = 0
    if config.security == 'confidential':
        linked_data_id = data_id

    name = Name(id = name_id,  name = participant_name, status = 0, data_id = linked_data_id) 
    db.session.add(name)
    db.session.commit()

    return participant, name


def get_last_data_id():
    last_data_id = db.session.query(func.max(Participant.id)).scalar()
    if last_data_id == None:
        print('No max data_id found in column; is this the first init?')
        last_data_id = 0
    return last_data_id


def get_name_id():
    # last_name_id = db.session.query(func.max(Name.name_id)).scalar()
    name_id = str(uuid.uuid4())
    while db.session.query(Name.id).filter_by(id = name_id).scalar() is not None:
        name_id = str(uuid.uuid4())
    return name_id


def get_experiment_order():
    order = random.sample(config.active, len(config.active))
    flattened_order = []
    for exp in order:
        if isinstance(exp, (list, tuple, set)):
            for subexp in exp:
                flattened_order.append(subexp)
        else:
            flattened_order.append(exp)

    return json.dumps(
        flattened_order
    )


def get_formatted_date(): # thanks to: https://www.programiz.com/python-programming/datetime/strftime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d-%H-%M-%S")
    

def get_next_experiment_condition(participant):
    exp = json.loads(participant.experiments)[int(participant.status)]

    last_insert_num = db.session.query(func.max(experiment_tables[exp].c.order)).scalar()

    if last_insert_num == None:
        last_insert_num = -1

    cnum = (last_insert_num+1) % len(config.experiments[exp]['conditions'])
    condition = config.experiments[exp]['conditions'][cnum]

    db.session.execute(
        experiment_tables[exp].insert().values(id = participant.id, condition = condition, order = last_insert_num + 1)
    )
    db.session.commit()

    return exp, condition


def decrypt_name(name):
    return encryptor.decrypt(name).decode()


def save_subject_data(location, data):
    with open(location + '.json', 'w') as file:
        json.dump(
            data, file, indent = 4
        )

def save_consent_form(name):
    now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    with open('./data/_consentforms_/' + now + '.txt', 'w') as file:

        with open('app/templates/consentform.html', 'r') as consentfile:
            file.write(consentfile.read())
        
        print('\n--------\n', file = file)
        print('date: ', now, file = file)
        print('\n--------\n', file = file)
        print('signature: ', name, file = file)