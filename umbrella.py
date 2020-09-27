import requests
import json
import base64
from requests.auth import HTTPBasicAuth
from cred import * 


class Tunnels:

    def __init__(self,host,key,secret,orgID):
        self.base_url = host
        self.key = key
        self.secret = secret
        self.orgID = orgID
        self.headers = {
                    "accept": "application/json",
                    "content-type": "application/json",
        }
        
    def getAllTunnels(self):
        url = f'{self.base_url}/{self.orgID}/tunnels'
        headers = self.headers
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(self.key, self.secret))
        if response.status_code != 200:
            raise Exception('Authentication failed')

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
        response = requests.delete(url, headers=headers, json=payload, auth=HTTPBasicAuth(self.key, self.secret))
        


class Devices(Tunnels):
    
    def getNetworkDevices(self):
        url = f'{self.base_url}/{self.orgID}/networkdevices'
        headers = self.headers
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(self.key, self.secret))

        if response.status_code != 200:
            raise Exception('Authentication failed')

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
        #response = requests.request("DELETE", url, headers=headers)



def main():
    # API endpoint
    host = "https://management.api.umbrella.com/v1/organizations"

    ## ORG1
    # SIG - Tunnels
    tunnelsORG1 = Tunnels(host,managementKey1,managemenetSecret1,orgID1)
    tunnelsORG1.getAllTunnels()
    # DNS - Network devices
    devicesORG1 = Devices(host,networkKey1,networkSecret1,orgID1)
    devicesORG1.getNetworkDevices()
    
    ## ORG2 
    # SIG - Tunnels
    #tunnelsORG2 = Tunnels(host,managementKey2,managemenetSecret2,orgID2)
    #tunnelsORG2.getAllTunnels()
     # DNS - Network devices

    
if __name__=='__main__':
    main()



