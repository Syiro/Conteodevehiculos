import json
import requests
import mysql.connector

class Enviar:
    def enviar(self,modo,red,brillo,cont,color,treshold,skipfps):
            
            self.modo=modo
            self.red=red
            self.brillo=brillo
            self.cont=cont
            self.color=color
            self.treshold=treshold
            self.skipfps=skipfps
                            # Conexión a la base de datos
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="Syiro2101.",
                database="mydb")

                # Crear cursor
            cursor = mydb.cursor()

                # Ejecutar la consulta
            cursor.execute("SELECT idusuarios FROM usuarios ORDER BY idusuarios DESC LIMIT 1;")
            result = cursor.fetchone()
            ultimoid=int(result[0])
            url = 'http://127.0.0.1:8000/configuracion/'
            pyload = {'idconfiguracion':ultimoid,'brillo':  self.brillo, 'contraste':  self.cont,
                    'color':  self.color, 'modo':  self.modo, 'redneuronal':  self.red , 'skipfps': self.skipfps , 'treshold': self.treshold}
            data=json.dumps(pyload)
            data2=json.dumps(pyload,indent=6,sort_keys=True,separators =(". ", " = "))
            response = requests.post(url, data)
            self.configactual(data2)
            self.filesave(data)
            if response.status_code == 200:
                print(response.content)
                
  
