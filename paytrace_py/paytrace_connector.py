import requests
import time

class APIError(Exception):
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return repr(self.value)

class PayTraceConnector:
    API_VERSION = 'v1'
    API_HOST = 'apitest2.paytrace.com'
    API_END_POINT = 'https://'+API_HOST+'/'


    def __init__(self,username,password,allow_insecure=False):
        """
            Create a new PayTrace Instance

            WARNING: The allow_insecure flag allows testing against a server without a valid SSL
            certificate.  Do not set to True for production data.
        """

        self.username = username
        self.password = password
        self.verify = not allow_insecure
        # verify communication with the API server
        self._ping()
        #authenticate with the server
        self._get_token()



    def _ping(self):
        """ Ping the API Server and check for a valid status message. """

        url = self.API_END_POINT+self.API_VERSION+'/ping'
        r = requests.get(url,verify=self.verify)
        if 200 != r.status_code:
            raise APIError("Unable to ping server. status code: "+str(r.status_code)+" response: "+r.text)
        json_response = r.json()
        if 'status' not in json_response:
            raise APIError("There was an error communicating with the PayTrace API. Missing status message from ping response.")
        elif json_response['status'] != 'success':
            raise APIError("There was an error communicating with the API. status = "+json_response['status'])
        return json_response


    def _get_token(self):
        """ Get an access token from the server for future API Calls """

        url = self.API_END_POINT+'oauth/token'
        data = {'grant_type':'password','username':self.username,'password':self.password}
        r = requests.post(url, data=data,verify=self.verify)
        if 200 != r.status_code:
            raise APIError("Unable to authentace with server: status_code: "+str(r.status_code)+" message: "+r.text)
        r_json = r.json()
        if 'access_token' not in r_json or 'token_type' not in r_json or 'expires_in' not in r_json:
            raise APIError("Invalid response, missing required values: "+str(r_json))
        self.token = r_json['access_token']
        self.token_type = r_json['token_type'].title() # capitalize "Bearer"
        self.token_expires = int(time.time()) -1 + int(r_json['expires_in'])

    def _get_custom_headers(self):
        return {
            'Host' : self.API_HOST,
            'Authorization': self.token_type+" "+self.token,
            'Content-Type' : 'application/json',
            'Cache-Control' : 'no-cache'
        }


    def keyed_sale(self,data):
        """ Submit a manually keyed transaction
        :data json data representing the transaction
            {
                  "amount": "1.00",
                  "credit_card": {
                    "number": "4111111111111111",
                    "expiration_month": "12",
                    "expiration_year": "2020"
                  },
                  "csc": "999",
                  "billing_address": {
                    "name": "Steve Smith",
                    "street_address": "8320 E. West St.",
                    "city": "Spokane",
                    "state": "WA",
                    "zip": "85284"
                  }
                }
        """

        url = self.API_END_POINT+self.API_VERSION+'/transactions/sale/keyed'
        headers = self._get_custom_headers()
        r = requests.post(url,json=data,headers=headers,verify=self.verify)
        if 200 != r.status_code:
            raise APIError("Unable to process keyed_sale: status_code: "+str(r.status_code)+" message: "+r.text)
        return r.json()
