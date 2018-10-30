import requests, datetime, json
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class IoTHub:
    
    def __init__ (self, gateId, endpoint, verifySslCertificate):
        self.gateId = gateId
        self.endpoint = endpoint
        self.baseUrl = endpoint + "/iot/v1"
        self.verifySslCertificate = verifySslCertificate

        self.httpClient = requests.Session()
        self.httpClient.headers.update({'Accept' : 'application/json'})
        self.httpClient.headers.update({'Content-Type' : 'application/json'})

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        print("IoTHub initialized")

    def activate(self, activationCode):
        print("IoTHub.activate({})".format(activationCode))
        url = self.baseUrl + "/activationrequest"
        payload = {'message' : {'activation_code' : activationCode , 'gate_id' : self.gateId }, 'timestamp' : self.getCurrentUTCTimestamp() }

        r = self.httpClient.post(url, data=json.dumps(payload), verify=self.verifySslCertificate)

        print("IoTHub.activate(..) returned {}".format(r.status_code))

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
