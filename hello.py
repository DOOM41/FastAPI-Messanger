import requests
from pprint import pprint

tok = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMiLCJleHAiOjE2ODA3Nzk0Mjl9.Z933oqo6HSIF0sxHNjx1DMmcAXWtrS4MrFHHjUpIMX4"
# a = requests.post(
#     'http://127.0.0.1:8000/create_chat/1',
#     headers={
#         'Authorization': f"Bearer {tok}"
#     }
# )


a = requests.post(
    'http://127.0.0.1:8000/send_message/1',
    headers={
        'Authorization': f"Bearer {tok}"
    },
    json={
        "content": "Hello bro!",
    }
)

# a = requests.get(
#     'http://127.0.0.1:8000/chat/my',
#     headers={
#         'Authorization': f"Bearer {tok}"
#     },
# )

pprint(a.json())