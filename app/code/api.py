from flask import Flask
from flask import request
from Adapter import Adapter
from InOutput import InOutput

app = Flask(__name__)

io = InOutput()

@app.route('/set_patient', methods=['POST'])
def set_patient():
    patientid = request.values.get('patientid')
    io.set_patient_by_id(patientid)
    return str(patientid)


@app.route('/personal_data', methods=['POST'])
def personal_data():
    return str(io.get_patient_personal_data())


@app.route('/icd_card', methods=['POST'])
def icd_card():
    return str(io.get_patients_icd_card())


@app.route('/pattern_patients', methods=['POST'])
def pattern_patients():
    return str(io.get_patients_by_pattern())


@app.route('/shorterm_death_prob', methods=['POST'])
def shorterm_death_prob():
    return str(io.get_quickly_death_model_point())


@app.route('/inpatient_mean', methods=['POST'])
def inpatient_mean():
    return str(cycle.get_average_of_inpatient_cycle_of_everypatient())


@app.route('/inpatient', methods=['POST'])
def inpatient():
    patientid = request.values.get('patientid')
    return str(cycle.get_inpatient_cycle_of_single_patient(patientid))
