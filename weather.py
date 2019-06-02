import requests
import re

def url_meteo_france(city, zipcode):
    return 'http://www.meteofrance.com/previsions-meteo-france/'+city.lower()+'/'+zipcode

def get(url):
    return requests.get(url)

def extract_meteo_france(body):
    data_to_extract = {
            "current-temperature": "day-summary-temperature",
            "sky": "day-summary-label",
            "UV": "day-summary-uv"
            }
    data = {}

    for k in data_to_extract.keys():
        data[k] = re.search(r"<li class=\""+data_to_extract[k]+"\"> ?(\w+ ?°?\w*)", body).group(1)
    return data

def extract(source, body):
    if(source == "meteo_france"):
        return extract_meteo_france(body)
    else:
        return {}

# use this function if you want current data for a location
# zipcode is required for meteo_france
def find(city, zipcode=''):
    sources = {"meteo_france": url_meteo_france(city, zipcode)}
    data = {}
    for k in sources.keys():
        resp = get(sources[k])
        if(resp.status_code == 200):
            data[k] = extract(k, resp.text)
        else:
            continue

    return data

