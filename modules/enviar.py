import json
import requests

class Enviar:
    def enviar(self,modo,red,brillo,cont,color,treshold,skipfps):
            self.modo=modo
            self.red=red
            self.brillo=brillo
            self.cont=cont
            self.color=color
            self.treshold=treshold
            self.skipfps=skipfps

            url = 'http://127.0.0.1:8000/configuracion/'
            pyload = {'brillo':  self.brillo, 'contraste':  self.cont,
                    'color':  self.color, 'modo':  self.modo, 'redneuronal':  self.red , 'skipfps': self.skipfps , 'treshold': self.treshold}
            data=json.dumps(pyload)
            data2=json.dumps(pyload,indent=6,sort_keys=True,separators =(". ", " = "))
            response = requests.post(url, data)
            self.configactual(data2)
            self.filesave(data)
            if response.status_code == 200:
                print(response.content)
            