from rest_framework.test import RequestsClient

client = RequestsClient()
response = client.get('https://town368.csie.ntu.edu.tw/v1.0/reports/1')
print(response.status_code)
