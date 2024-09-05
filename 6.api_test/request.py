import requests

url = "http://127.0.0.1:5000/api"
files = {
    "students": open("resource/students.csv", "r"),
    "cars": open("resource/cars.csv", "r"),
}
print(files)
response = requests.post(url, files=files)
with open("resource/solution_requests.csv", "w") as f:
    f.write(response.text)
