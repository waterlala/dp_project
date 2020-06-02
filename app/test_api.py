import requests

payload = {'patientid': '0007613eee440aa3145f09e1dfd0865b'}
res = requests.post('http://127.0.0.1:5000/set_patient', data=payload)
print(f'set_patient: {res.text}')

res = requests.post('http://127.0.0.1:5000/personal_data')
print(f'personal_data: {res.text}')

res = requests.post('http://127.0.0.1:5000/icd_card')
print(f'icd_card: {res.text}')

res = requests.post('http://127.0.0.1:5000/pattern_patients')
print(f'pattern_patients: {res.text}')

res = requests.post('http://127.0.0.1:5000/shorterm_death_prob')
print(f'shorterm_death_prob: {res.text}')

res = requests.post('http://127.0.0.1:5000/inpatient_mean')
print(f'inpatient_mean: {res.text}')

res = requests.post('http://127.0.0.1:5000/inpatient', data=payload)
print(f'inpatient: {res.text}')

input()
