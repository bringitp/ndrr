import requests
import json
#url = "https://ron-the-rocker.net/ndrr/rooms/1/messages"
url = "http://localhost:7777/rooms/1/messages"
#url = "http://localhost:7777"

headers = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJNY2EzYmd2SG50eEtrYlJUdUFnU3dDT2NGbURuYUFpa0JKWVh3dndoVHJVIn0.eyJleHAiOjE2OTI4OTI1MTksImlhdCI6MTY5Mjg1NjUxOSwianRpIjoiZGE0NjRjNGYtZTZjOS00ZjkwLTg3ZDEtNWRkNjllMzkzZGRhIiwiaXNzIjoiaHR0cHM6Ly9yb24tdGhlLXJvY2tlci5uZXQvYXV0aC9yZWFsbXMvbmRyciIsInN1YiI6IjM3NDc1Y2JhLWY4YTctNDdmMy1hZGI5LTc1Y2EwOWMxYWZhNCIsInR5cCI6IkJlYXJlciIsImF6cCI6InB5dGhvbi1jbGllbnQiLCJzZXNzaW9uX3N0YXRlIjoiZTU2OTVhZWItMjc1ZS00NDUyLTliNDUtYjgzMTIxZTU4YTg3Iiwic2NvcGUiOiIiLCJzaWQiOiJlNTY5NWFlYi0yNzVlLTQ0NTItOWI0NS1iODMxMjFlNThhODcifQ.QEyFb2NSGCK8fiCAZS8au6eycXwzaD95lQ0laA_QheQgb5eDBYXosfq9SI0GTjitvNNYWCRuQNJLCbW7ZCQsuMEm7HwThdEKlDM7cg-gCYfPrXIt6EWA02BYyOhuzCQPoF_VkyUPjWle4SoD416SJzKazGkK_cFwzrisijztqTSAdlRhWsKp1hc17zJ3QWQtRxliI7miMNpLeisPC25QTJ49gQ5pF2jJTGsRyODSwdqgvNvgTYF4weRUPZRIOKSJHw4O8exwGCMxiKfBQWo_xdhJmXITrL6sfWcmqVBvTsEEBiD03QYE_l3FNP_5NXCbF5HvofcGJ6fkUhhJeYH4bQ"
   } 
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    formatted_json = json.dumps(data, indent=4, ensure_ascii=False)
    print(formatted_json)
else:
    print("Error:", response.status_code) 
    print("Error:", response.text) 
