import requests

url = "http://localhost:7777/rooms/1/messages?skip=0&limit=10"
headers = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJhemxKdHZFUUFQR09FTVlnWDhUd1FTYWt3ZHZveUIzZVRSTGRTMUd0dWFvIn0.eyJleHAiOjE2OTI2MzA0ODYsImlhdCI6MTY5MjU5NDQ4NiwianRpIjoiMzkzZjdlNTQtY2VkMC00MWU3LTkyYzQtNjJlNWEwOTcyNTJjIiwiaXNzIjoiaHR0cHM6Ly9yb24tdGhlLXJvY2tlci5uZXQvYXV0aC9yZWFsbXMvbmRyciIsInN1YiI6IjJhY2E5NTZhLWM0ZjAtNGFmNy1iNzhmLWFiMzNlN2E2ZWExMyIsInR5cCI6IkJlYXJlciIsImF6cCI6InB5dGhvbi1jbGllbnQiLCJzZXNzaW9uX3N0YXRlIjoiMDQzMWExNDYtZjYwMi00ODM4LWFlMjctZTFkNWEwMzJjYTYyIiwic2NvcGUiOiIiLCJzaWQiOiIwNDMxYTE0Ni1mNjAyLTQ4MzgtYWUyNy1lMWQ1YTAzMmNhNjIifQ.aPRfRcF-5p7mQfcGOg07EPDLS3kJFcO73OMDRsqycwcpyE4SffTgxnO2p0fCobPv3p21sbuExzr9S4cNsIGy9uMFsBmEYZrRGJ7kNtwUQVLIhs6LPNErykYKap5FHrbWgK_WD_fspz2-x2UHpZHb4Lft0B5SYTDQReIdwkKpUKGO9FRsMUHH2-DHcNSXjtpR2Xu-IS3Q9mX2woj9LZ44QhRtpvQDg10_6HULwkvmurwXhfneVxPx3AiD1V7dhvUic9EY5rp0NY9nULYuDF86goLfIqWp6NpAtECvnxkoZ21dk-iAofZxmb25W7LZuTa1lT6tr6Sxu92ZVDsFS3Q0Ug"
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Error:", response.status_code) 
