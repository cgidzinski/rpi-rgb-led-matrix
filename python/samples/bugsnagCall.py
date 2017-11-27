import sys
import requests
import json
import yaml

projectID = ""
token = ""
data=[]

def setup():
    global projectID, token
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        projectID = cfg['bugsnag']['project']
        token = cfg['bugsnag']['token']

def getData():
    return data

def hydrate(errorType):
    global data
    print "Finding "+errorType+" Errors"
    url = 'https://api.bugsnag.com/projects/'+projectID+'/errors?sort=last_seen&direction=desc&filters[error.status][][value]='+errorType+'&filters[error.status][][type]=eq'
    headers = {'Authorization': 'token '+token, 'X-Version':'2'}
    r = requests.get(url, headers=headers)
    data = json.loads(r.text)
    return True

if __name__ == "__main__":
    test()
