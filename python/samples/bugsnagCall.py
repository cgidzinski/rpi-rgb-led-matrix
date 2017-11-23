import sys
import requests
import json
import yaml

projectName = ""
orgName = ""
token = ""

def setup():
    global projectName, orgName, token
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        projectName = cfg['bugsnag']['project']
        orgName = cfg['bugsnag']['organization']
        token = cfg['bugsnag']['token']

def findOrg():
    print "Finding Organization"
    url = 'https://api.bugsnag.com/user/organizations?per_page=10'
    headers = {'Authorization': 'token '+token, 'X-Version':'2'}
    r = requests.get(url, headers=headers)
    json_data = json.loads(r.text)
    for item in json_data:
        if item["name"] == orgName:
            print item['id']
            return item['id']
    return -1

def findProject(orgID):
    print "Finding Project"
    offset = ""
    while True: 
        url = 'https://api.bugsnag.com/organizations/'+orgID+'/projects?direction=asc&per_page=100&sort=created_at'
        if offset != "":
            url = 'https://api.bugsnag.com/organizations/'+orgID+'/projects?direction=asc&offset[null_sort_field]=false&offset[sort_field_offset]='+offset+'&per_page=100&sort=created_at'
        headers = {'Authorization': 'token '+token, 'X-Version':'2'}
        r = requests.get(url, headers=headers)
        json_data = json.loads(r.text)
        if len(json_data) == 0:
            return -1
        for item in json_data:
            offset = item['id']
            if item['name'] == projectName:
                print item['id']
                return item['id']
    return -1

def findErrors(projID, errorType):
    print "Finding "+errorType+" Errors"
    url = 'https://api.bugsnag.com/projects/'+projID+'/errors?sort=last_seen&direction=desc&filters[error.status][][value]='+errorType+'&filters[error.status][][type]=eq'
    headers = {'Authorization': 'token 215cca6a-9557-4031-b245-fb5b1ff6de27', 'X-Version':'2'}
    r = requests.get(url, headers=headers)
    json_data = json.loads(r.text)
    if len(json_data) != 0:
        print "Found Errors"
        return json_data
    else:
        return -1

if __name__ == "__main__":
    test()
