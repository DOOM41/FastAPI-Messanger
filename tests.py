import requests

tok = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiYXVkIjpbImZhc3RhcGktdXNlcnM6YXV0aCJdLCJleHAiOjE2ODA4NDkxOTV9.VcHJ7QfIxRA1gMj9EVCUWLhMqV0xxKGKnamdLBhDHA4'


# a = requests.get(
#     'http://127.0.0.1:8000/chat/?user_id=2',
#     headers={
#     "Authorization": f"Bearer {tok}"
#     },
# )

a = requests.get(
    'http://127.0.0.1:8000/chat/my',
    headers={
        "Authorization": f"Bearer {tok}"
    },
)

print(a.json())