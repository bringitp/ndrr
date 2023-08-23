import requests

url = "http://localhost:7777/rooms/1/messages"
headers = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJNY2EzYmd2SG50eEtrYlJUdUFnU3dDT2NGbURuYUFpa0JKWVh3dndoVHJVIn0.eyJleHAiOjE2OTI3ODEwMzYsImlhdCI6MTY5Mjc0NTAzNiwianRpIjoiZGUwYzY1ZmMtN2U0Mi00OWQxLTgyYzktMjYwY2U5MDY4YTIwIiwiaXNzIjoiaHR0cHM6Ly9yb24tdGhlLXJvY2tlci5uZXQvYXV0aC9yZWFsbXMvbmRyciIsInN1YiI6IjM3NDc1Y2JhLWY4YTctNDdmMy1hZGI5LTc1Y2EwOWMxYWZhNCIsInR5cCI6IkJlYXJlciIsImF6cCI6InB5dGhvbi1jbGllbnQiLCJzZXNzaW9uX3N0YXRlIjoiMzAyYjY5ZmItYWQ4ZS00MDgyLWI3Y2ItMTc4NGU1OWVhZGQ5Iiwic2NvcGUiOiIiLCJzaWQiOiIzMDJiNjlmYi1hZDhlLTQwODItYjdjYi0xNzg0ZTU5ZWFkZDkifQ.qZNkIu772JLdvH16ZfAPNC9dUcfEcDBKrFCljC7hcT6huKhnPpdpatRzFVBJvDePmsGVMtUoANQZarLlqETcSaqqCmcowhyLMiXYJ2YNY3YGKfxYlnB1k1u9yQnukAhlf6UeKThL1mgePZ9Z-lXgxJYQUf7ERG5CAtwH9J6xzsxlrham-L3V56swARhFPguV0rF-TPDd-FNIOgTBCmSJdhhVJBLhPhrsIwHT8uWOp0a2nHQUL2IfyjWfuvszulWgeWDUEp9Kxr8NnTHD4Vw19R_ODzt2i1OE1PBgyzU5kiGaH56338CDGUxUEFj4wCCA52CEznsuj6RjkJnHcnJYWw",
    "Content-Type": "application/json"
}

data = {
    "message_content": "あまり食欲わかない暑さですね"
}

response = requests.post(url, json=data, headers=headers)

if response.status_code != 200:
    print("Request failed with status code:", response.status_code)
    print("Error response:", response.text)
else:
    try:
        response_json = response.json()
        print("Response:", response.status_code, response_json)
    except requests.exceptions.JSONDecodeError:
        print("Response does not contain valid JSON data.")
