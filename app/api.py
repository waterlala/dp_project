from flask import Flask
from flask import request
from flask import render_template

from adapter import Adapter


app = Flask(__name__)

#auto reload
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

adapter = Adapter()

#需全改 變數用IO class  但是需傳進adapter轉json
@app.route('/set_patient', methods=['POST'])
def set_patient():
    adapter.set_patient(request)

@app.route('/personal_data', methods=['POST'])
def personal_data():
    adapter.personal_data()

@app.route('/icd_card', methods=['POST'])
def icd_card():
    adapter.icd_card()

@app.route('/pattern_patients', methods=['POST'])
def pattern_patients():
    adapter.pattern_patients()

@app.route('/shorterm_death_prob', methods=['POST'])
def shorterm_death_prob():
    adapter.shorterm_death_prob()

@app.route('/inpatient_mean', methods=['POST'])
def inpatient_mean():
    adapter.inpatient_mean()


@app.route('/inpatient', methods=['POST'])
def inpatient():
    adapter.inpatient(request)

@app.route("/")
def web_main(): 
    adapter.web_main(render_template)
