import sys
import requests
import json
import yaml

repo = ""
username = ""
token = ""

def setup():
    global projectName, repo, token
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        repo = cfg['github']['repo']
        username = cfg['github']['username']
        token = cfg['github']['token']

def test():
    setup()
    url = 'https://api.github.com/repos/Shopify/flow/labels/1589'
    r = requests.get(url, auth=(username,token))
    json_data = json.loads(r.text)
    print json_data

def findPR():
    url = 'https://api.github.com/repos/'+repo+'/pulls'
    r = requests.get(url, auth=(username,token))
    json_data = json.loads(r.text)
    return json_data

def findReviews(pull):
    url = 'https://api.github.com/repos/'+repo+'/pulls/'+str(pull)+'/reviews'
    r = requests.get(url, auth=(username,token))
    json_data = json.loads(r.text)
    return json_data


if __name__ == "__main__":
    test()
