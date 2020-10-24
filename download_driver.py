import requests 
def start(url,location):
    r = requests.get(url, stream=True)
    with open(location, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
