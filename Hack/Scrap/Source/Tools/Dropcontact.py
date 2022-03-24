from json import dump, dumps
import json
import requests

class Dropcontact():
    def __init__(self):
        self.apikey = 'kPGaCSI8hmTe8cICYjFwDbNzXVOy8X'

    def perepareRequest(self,data):
        result = ''
        dataToSend = self.constructData(data)
        print(len(dataToSend))
        try:
            print('OK----------------')
            # for sendData in dataToSend:
            #     requette = requests.post(
            #         "https://api.dropcontact.io/batch",
            #         json = {
            #             'data': sendData,
            #             'siren': True,
            #             'language': 'fr'
            #         },
            #         headers={
            #             'Content-Type': 'application/json',
            #             'X-Access-Token': self.apikey
            #         }
            #     )
            #     print(requette.text,'----wawa')
            #     value = json.loads(requette.text)
            #     print(requette.text,' json-------')
            #     result = value['request_id']
            #     print(result,'result----------------')
        except Exception as e:
            print(e)

        return result

    def executeRequest(self,data):
        request_id = self.perepareRequest(data)
        data = ''
        if request_id != '':
            try:
                req = requests.get("https://api.dropcontact.io/batch/"+request_id,headers={
                    'X-Access-Token': self.apikey
                })
                data = json.loads(req.text)
            except Exception as e:
                print(e)
        return data

    def constructData(self,data):
        tabData = []
        result = []
        compteur = 1
        for d in data:
            val = {
                'first_name': d['prenom'],
                'last_name': d['nom'],
                'website': d['site'],
            }
            tabData.append(val)
            compteur = compteur + 1
            if compteur == 250:
                result.append(tabData)
                tabData = []
                compteur = 1
        return result
        