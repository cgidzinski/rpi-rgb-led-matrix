import sys
import requests
import json
import yaml

projectID = ""
token = ""

def setup():
    global projectID, token
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        projectID = cfg['bugsnag']['project']
        token = cfg['bugsnag']['token']

def findErrors(errorType):
    print "Finding "+errorType+" Errors"
    url = 'https://api.bugsnag.com/projects/'+projectID+'/errors?sort=last_seen&direction=desc&filters[error.status][][value]='+errorType+'&filters[error.status][][type]=eq'
    headers = {'Authorization': 'token '+token, 'X-Version':'2'}
    r = requests.get(url, headers=headers)
    json_data = json.loads(r.text)
    if len(json_data) != 0:
        print "Found Errors"
        print json_data
        return json_data
    else:
        return -1

if __name__ == "__main__":
    test()
