import sys
import requests
import json
import yaml

projectID = ""
token = ""
data={'new':[],'open':[],'in_progress':[],'ignored':[]}
ready = False
def setup():
    global projectID, token
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        projectID = cfg['bugsnag']['project']
        token = cfg['bugsnag']['token']

def isReady():
    return ready

def getData():
    return data

def hydrate():
    global data, ready
    data = []
    print "Getting Bugsnag Data"
    for errorType in data:
        url = 'https://api.bugsnag.com/projects/'+projectID+'/errors?sort=last_seen&direction=desc&filters[error.status][][value]='+errorType+'&filters[error.status][][type]=eq'
        headers = {'Authorization': 'token '+token, 'X-Version':'2'}
        r = requests.get(url, headers=headers)
        data[errorType] = json.loads(r.text)
    print "Got Bugsnag Data"
    ready = True
    return

if __name__ == "__main__":
    test()
