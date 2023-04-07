import requests

tok = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiYXVkIjpbImZhc3RhcGktdXNlcnM6YXV0aCJdLCJleHAiOjE2ODA4NDU0NTJ9.Y5QDh5yr0dWxck6YIxue9AE94sR59GlRyRJmYAGxclA'


a = requests.get(
    'http://127.0.0.1:8000/chat/?user_id=2',
    headers={
    "Authorization": f"Bearer {tok}"
    },
)

print(a.json())