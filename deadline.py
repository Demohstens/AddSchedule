import json

string  = '{ "username":"WallacMat", "password" : "20050204", "server": "tritone.webuntis.com", "school" : "Angell-Akademie", "useragent" :"Matts Website backend", "secret_key" : "nhS+t;Vm9p7TcYm#[zY5^rC&gYSK.6B>CZD!kjFpd%z"}'

print(json.loads(string))