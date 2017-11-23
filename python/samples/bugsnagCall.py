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

def test():
    print "Searching for organization: " + orgName
    org = findOrg()
    if org == -1:
        print("No Organization Found")
        sys.exit()
    print("Found " + orgName + ' @ ' + org)

    print "Searching for project: " + projectName
    proj = findProject(org)
    if proj == -1:
        print("No Project Found")
        sys.exit()
    print("Found " + projectName + ' @ ' + proj)
    print "" 
    print "New Errors"
    print "-------------------------------"
    findErrors(proj,"new")

    print "Open Errors"
    print "-------------------------------"
    findErrors(proj,"open")

def findOrg():
    url = 'https://api.bugsnag.com/user/organizations?per_page=10'
    headers = {'Authorization': 'token '+token, 'X-Version':'2'}
    r = requests.get(url, headers=headers)
    json_data = json.loads(r.text)
    for item in json_data:
        if item["name"] == orgName:
            return item['id']
    return -1

def findProject(orgID):
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
                return item['id']
    return -1

def findErrors(projID, errorType):
    url = 'https://api.bugsnag.com/projects/'+projID+'/errors?sort=last_seen&direction=desc&filters[error.status][][value]='+errorType+'&filters[error.status][][type]=eq'
    headers = {'Authorization': 'token 215cca6a-9557-4031-b245-fb5b1ff6de27', 'X-Version':'2'}
    r = requests.get(url, headers=headers)
    json_data = json.loads(r.text)
    if len(json_data) != 0:
        return json_data
    else:
        return -1
    #for error in json_data:
       #print error['error_class']
        #print error['message']
        #print error['last_seen']
        #print error 
        #print "" 


if __name__ == "__main__":
    test()
