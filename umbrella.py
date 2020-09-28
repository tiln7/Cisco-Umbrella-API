import requests
import json
from cred import * 
import sys


class Tunnels:
    def __init__(self,host,organization):
        self.base_url = host
        self.mngmt_key = organization.mngmt_key
        self.network_key = organization.network_key
        self.mngmt_secret = organization.mngmt_secret
        self.network_secret = organization.network_secret
        self.orgID = organization.org_id
        self.headers = {
                    "accept": "application/json",
                    "content-type": "application/json",
        }

    def getAllTunnels(self):
        url = f'{self.base_url}/{self.orgID}/tunnels'
        headers = self.headers
        try:
            response = requests.get(url, headers=headers, auth=(self.mngmt_key, self.mngmt_secret))  
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        tunnels = json.loads(response.text)
        if len(tunnels) > 0:
            # Loop through tunnels 
            for tunnel in tunnels:
                # Get ID of each tunnel
                tunnelId = tunnel["id"]
                print(tunnelId)
                # Delete selected tunnel
                self.deleteAllTunnels(tunnelId)

    def deleteAllTunnels(self,tunnelID):
        url = f'{self.base_url}/{self.orgID}/tunnels/{tunnelID}'
        payload = {"detachPolicies": True}
        headers = self.headers
        #response = requests.delete(url, headers=headers, json=payload, auth=HTTPBasicAuth(self.mngmt_key, self.mngmt_secret))
        

class Devices(Tunnels):
    
    def getNetworkDevices(self):
        url = f'{self.base_url}/{self.orgID}/networkdevices'
        headers = self.headers

        try:
            response = requests.get(url, headers=headers, auth=(self.network_key, self.network_secret))  
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        devices = json.loads(response.text)
        if len(devices) > 0:
            # Loop through devices
            for device in devices:
                originID = device["originId"]
                print(originID)
                self.deleteAllDevices(originID)
                
    def deleteAllDevices(self, originID):
        url = f'{self.base_url}/{self.orgID}/networkdevices/{originID}'
        headers = self.headers
        #response = requests.request("DELETE", url, headers=headers, auth=(self.network_key, self.network_secret))


class Organization():
    def __init__(self, org):
        self.mngmt_key = self.import_mngmt_key(org)
        self.network_key = self.import_network_key(org)
        self.mngmt_secret = self.import_mngmt_secret(org)
        self.network_secret = self.import_network_secret(org)
        self.org_id = self.import_org_id(org)

    def import_mngmt_key(self, org):
        if org == "org1":
            return managementKey1
        elif org == "org2":
            return managementKey2
    def import_network_key(self, org):
        if org == "org1":
            return networkKey1
        elif org == "org2":
            return networkKey2
    def import_mngmt_secret(self, org):
        if org == "org1":
            return managemenetSecret1
        elif org == "org2":
            return managemenetSecret2
    def import_network_secret(self, org):
        if org == "org1":
            return networkSecret1
        elif org == "org2":
            return networkSecret2
    def import_org_id(self, org):
        if org == "org1":
            return orgID1
        elif org == "org2":
            return orgID2
    

def main():
    # API endpoint
    host = "https://management.api.umbrella.com/v1/organizations"

    orgList = []

    for x in range(1, len(sys.argv)):
        # Initialize object org
        org = Organization(sys.argv[x])
        # Append it to orgList
        orgList.append(org)

    # Loop through list of initialized objects
    for x in orgList:
        # Initialize objects tunnelsORG and devicesORG and call methods on them (object "org" is an argument)
        tunnelsORG = Tunnels(host,x)
        tunnelsORG.getAllTunnels()
        devicesORG = Devices(host,x)
        devicesORG.getNetworkDevices()    

    
if __name__=='__main__':
    main()



