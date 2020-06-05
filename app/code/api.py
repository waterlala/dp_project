from flask import Flask
from flask import request
from Adapter import Adapter
from InOutput import InOutput

app = Flask(__name__)

io = InOutput()
df_json_adapter = Adapter(io)

@app.route('/personal_data', methods=['POST'])
def personal_data():
    patientid = request.values.get('patientid')
    return str(df_json_adapter.handle_instructions("get_personal_info",patientid))

@app.route('/icd_card', methods=['POST'])
def icd_card():
    patientid = request.values.get('patientid')
    return str(df_json_adapter.handle_instructions("get_icd_category_growth_trend",patientid))

@app.route('/inpatient', methods=['POST'])
def inpatient():
    patientid = request.values.get('patientid')
    return str(df_json_adapter.handle_instructions("get_personal_inpatient_cycle",patientid))

@app.route('/inpatient_mean', methods=['POST'])
def inpatient_mean():
    return str(df_json_adapter.handle_instructions("get_average_of_all_the_patients_cycles",""))

@app.route('/shorterm_death_prob', methods=['POST'])
def shorterm_death_prob():
    patientid = request.values.get('patientid')
    return str(df_json_adapter.handle_instructions("get_shortterm_mortality_rate",patientid))

@app.route('/pattern_patients', methods=['POST'])
def pattern_patients():
    patientid = request.values.get('patientid')
    return str(df_json_adapter.handle_instructions(,patientid))




