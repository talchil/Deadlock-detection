import requests

r = requests.get("https://phimxxx.ai/chich-em-di-lon-mup-ngon-muon-ban-suong-lut-can-khieu-goi/")
with open("black.html", "w", encoding="utf-8") as f:
    f.write(r.text)

