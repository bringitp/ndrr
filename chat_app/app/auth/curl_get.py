import requests
import json
url = "https://ron-the-rocker.net/ndrr/rooms/1/messages"
#url = "http://localhost:7777/rooms/1/messages"
#url = "http://localhost:7777"

headers = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJNY2EzYmd2SG50eEtrYlJUdUFnU3dDT2NGbURuYUFpa0JKWVh3dndoVHJVIn0.eyJleHAiOjE2OTI4NzM5NTQsImlhdCI6MTY5MjgzNzk1NCwianRpIjoiOTA1ZTJlMzUtODRmZS00NDU2LWI0YjItMTMyOTBjNDZkY2RhIiwiaXNzIjoiaHR0cHM6Ly9yb24tdGhlLXJvY2tlci5uZXQvYXV0aC9yZWFsbXMvbmRyciIsInN1YiI6IjM3NDc1Y2JhLWY4YTctNDdmMy1hZGI5LTc1Y2EwOWMxYWZhNCIsInR5cCI6IkJlYXJlciIsImF6cCI6InB5dGhvbi1jbGllbnQiLCJzZXNzaW9uX3N0YXRlIjoiNTk3NWRiOGEtMzY3MC00ODExLTkzYmItMDRhYzE3MDY0MjQ2Iiwic2NvcGUiOiIiLCJzaWQiOiI1OTc1ZGI4YS0zNjcwLTQ4MTEtOTNiYi0wNGFjMTcwNjQyNDYifQ.HIQGV6UG1znI81Zswm3wyBPvEPI3P_Zt1ckksoUPAGdvOFeeO4UG2JW7DXiQa96BsuHq9Nwv7__A5TGeNiimsnln3qjUR_15SXBbd-udQZlfOYMZ6TB_LDoYLbFj9kXZ3rFOjP6IchatRQoIDsbBPIv8vBlFN1ekBMv57pnpn1EeUBDGrDIGJp_wCO8PQQDB3gMKhtyu4VZVJsGGizsFYlpWxnR3dPG--DWaJPd2Op3ObrN0f2IxSx4DMiis8Sb8tMDFhd31zYkrFwHX_KKZpbnGEY5an15_f76Lut08OGwyI8pzpip9uEq-_Vf0_aBBjNVxAN5Hgn0zyRjIlQTbp"
    }

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    formatted_json = json.dumps(data, indent=4, ensure_ascii=False)
    print(formatted_json)
else:
    print("Error:", response.status_code) 
    print("Error:", response.text) 
