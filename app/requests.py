import requests

def random_post():
    url='http://quotes.stormconsultancy.co.uk/random.json'
    pos= requests.get(url)
    posts= pos.json()
    return posts