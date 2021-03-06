import requests


def print_response(response):
    print('STATUS CODE ', response.status_code)
    print()
    print('TEXT ', response.text)
    print()

print_response(requests.post('http://127.0.0.1:8000/tweets', {'tweet': 'Test 1'}))
print_response(requests.post('http://127.0.0.1:8000/tweets', {'tweet': 'Test 2'}))
r = requests.get('http://127.0.0.1:8000/tweets')
print_response(r)

rl = r.json()

for r in rl:
    print_response(requests.delete('http://127.0.0.1:8000/tweets/' + r['id']))


print_response(requests.get('http://127.0.0.1:8000/tweets'))

