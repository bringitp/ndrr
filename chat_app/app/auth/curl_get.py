import requests
import json
url = "https://ron-the-rocker.net/ndrr/rooms/1/messages"
#url = "http://localhost:7777/rooms/1/messages"
#url = "http://localhost:7777"

headers = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJNY2EzYmd2SG50eEtrYlJUdUFnU3dDT2NGbURuYUFpa0JKWVh3dndoVHJVIn0.eyJleHAiOjE2OTI4ODg5OTYsImlhdCI6MTY5Mjg1Mjk5NiwianRpIjoiZTU4MmFhMDQtYmM2My00NzhiLWI0OWYtZjBiYWU4ZmU5ODUyIiwiaXNzIjoiaHR0cHM6Ly9yb24tdGhlLXJvY2tlci5uZXQvYXV0aC9yZWFsbXMvbmRyciIsInN1YiI6IjM3NDc1Y2JhLWY4YTctNDdmMy1hZGI5LTc1Y2EwOWMxYWZhNCIsInR5cCI6IkJlYXJlciIsImF6cCI6InB5dGhvbi1jbGllbnQiLCJzZXNzaW9uX3N0YXRlIjoiNGNkZmY4MmUtODNhOS00YThkLThjZTktMDUyMGE2OTk4NDhlIiwic2NvcGUiOiIiLCJzaWQiOiI0Y2RmZjgyZS04M2E5LTRhOGQtOGNlOS0wNTIwYTY5OTg0OGUifQ.SG4LvqUY-4xdfbuIpp7pU6k542-C3aGe454WZ5sg-8PWAr4o26TLQCXuQlFYqD6GWlwxEDV89GNVW3KFsr30x6hbqmLV4MWxxv-RZ2vno7kmw74kZEXuR1DeLkeq7e1jszzlLA9QFKmD5cCymkmBONQzzJyDGmcaAkadu4DoRLz1IuFETE89__QpQhKb10obsqUNE79pU6uxSlg93wzgtv9ZH9jqnuEE8bmPdO4kpp1RKCGtT5vkCTJws2CMx5b7Fd6985lzwBCEfmL7OUNxmIrVKeOem3gjbmUCsA47-HxCDawDyHG5xEZ3pJjx4GJTATDVw-_30cDkXIHKrKyABg"    }

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    formatted_json = json.dumps(data, indent=4, ensure_ascii=False)
    print(formatted_json)
else:
    print("Error:", response.status_code) 
    print("Error:", response.text) 
