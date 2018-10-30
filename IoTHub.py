import requests, datetime, json
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class IoTHub:
    
    def __init__ (self, gateId, endpoint, verifySslCertificate):
        self.gateId = gateId
        self.endpoint = endpoint
        self.baseUrl = "https://iothub-" + endpoint + "/iot/v1"
        self.verifySslCertificate = verifySslCertificate

        self.httpClient = requests.Session()
        self.httpClient.headers.update({'Accept' : 'application/json'})
        self.httpClient.headers.update({'Content-Type' : 'application/json'})
        
        self.httpAuthClient = requests.Session()
        self.httpAuthClient.headers.update({'Accept' : 'application/json'})
        self.httpAuthClient.headers.update({'Content-Type' : 'application/x-www-form-urlencoded'})
        self.authUrl = "https://identity-" + endpoint

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        print("IoTHub initialized")

    def requestAuthorization(self):
        print("IoTHub.requestAuthorization()")
        url = self.authUrl + "/connect/deviceauthorization"
        payload = 'client_id=axoom-device'

        r = self.httpAuthClient.post(url, data=payload, verify=self.verifySslCertificate)
        print("IoTHub.requestAuthorization(..) returned {}".format(r.status_code))
        
        if r.status_code == 200:
            self.deviceauthorization = r.json()
            return true
        
        return false

    def requestToken(self):
        print("IoTHub.requestToken()")
        url = self.authUrl + "/connect/token"
        payload = 'client_id=axoom-device&grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Adevice_code&device_code=' + self.deviceauthorization['device_code']
        
        r = self.httpAuthClient.post(url, data=payload, verify=self.verifySslCertificate)
        
        if r.status_code == 200:
            print("IoTHub.requestToken(..) returned 200")
            self.httpClient.headers.update({'Authorization' : r.json()['token_type'] + ' ' + r.json()['access_token']})
            return '';
        else:
            print("IoTHub.requestToken(..) returned {statusCode} with error: {error}".format(statusCode=r.status_code, error=r.json()['error']))
            return error=r.json()['error'];
        
    def heartbeat(self):
        print("IoTHub.heartbeat()")
        
        url = self.baseUrl + "/gates/" + self.gateId + "/alive"
        payload = {'timestamp' : self.getCurrentUTCTimestamp() }
                
        r = self.httpClient.post(url, data=json.dumps(payload), verify=self.verifySslCertificate)
        
        print("IotHub.heartbeat() returned {}".format(r.status_code))

    def observe(self, datastreamId, value):
        print("IoTHub.observe({}, {})".format(datastreamId, value))
        
        url = self.baseUrl + "/datastream/" + datastreamId + "/observation"
        timestamp = self.getCurrentUTCTimestamp()
        payload = {'message' : {'value' : value,  'timestamp' : timestamp }, 'timestamp' : timestamp }
        
        r = self.httpClient.post(url, data=json.dumps(payload), verify=self.verifySslCertificate)

        print("IoTHub.observe(..) returned {}".format(r.status_code))

    def getCurrentUTCTimestamp(self):
       return "{}Z".format(datetime.datetime.utcnow().isoformat())
