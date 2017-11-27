import sys
import requests
import json
import yaml

repo = ""
username = ""
token = ""
data = []
ready = False
def setup():
    global projectName, repo, token
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        repo = cfg['github']['repo']
        username = cfg['github']['username']
        token = cfg['github']['token']

def getData():
    return data

def isReady():
    return ready

def hydrate():
    global data, ready
    url = 'https://api.github.com/repos/'+repo+'/pulls'
    print "Getting Github Data"
    r = requests.get(url, auth=(username,token))
    PR_data = json.loads(r.text)
    for pr in PR_data:
        newPR =  {'approvals':0,'labels':[], 'number':pr['number'], 'title':pr['title'], 'user':pr['user']['login']}
        url = 'https://api.github.com/repos/'+repo+'/pulls/'+str(pr['number'])+'/reviews'
        r = requests.get(url, auth=(username,token))
        REV_data = json.loads(r.text)
        print pr['number']
        for review in REV_data:
            print review
            print " "
            newPR['approvals'] += 1
        url = 'https://api.github.com/repos/'+repo+'/issues/'+str(pr['number'])
        r = requests.get(url, auth=(username,token))
        ISS_data = json.loads(r.text)
        for label in ISS_data['labels']:
            newPR['labels'].append(label['name'])
        data.append(newPR)
    print "Got Github Data"
    ready = True
    return 

if __name__ == "__main__":
    findPRS()
