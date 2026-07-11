import requests

# We need to simulate the login to get the cookie
session = requests.Session()
login_data = {
    "username": "admin",
    "password": "password" # Wait, what is the admin password? Let's assume it failed because of auth.
}
# Actually I'd better just make a request and see what it is
res = requests.post("http://localhost:8000/beds/wards", json={"name": "Test Ward", "type": "General", "capacity": 10})
print("No auth response:", res.status_code, res.text)
