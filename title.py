import requests

r=requests.get("https://vnexpress.net/")

print(r.url)
print(r.connection)
print(r.cookies)
print(r.encoding)
print(r.headers)
print(r.history)
print(r.is_permanent_redirect)
print(r.is_redirect)
print(r.ok)
print(r.links)
print(r.content)

