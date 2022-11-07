from untitled import *
import asyncio
import uvicorn
from app import models,main,schemas,Conexion
import requests
import json

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self) 
        
        self.radioButton_2.toggled.connect(self.modo)
        self.pushButton_4.clicked.connect(self.enviar)
        
    def modo(self,selected):
        if selected:
            a="Tiempo real"
    
    def enviar(self):
        url = 'http://127.0.0.1:8000/configuracion/'
        pyload = {'brillo':300,'contraste':10,'color':23,'modo':'prueba','redneuronal':'Movilnet2'}
        
        response = requests.post(url, data=json.dumps(pyload))
        print(response.url)
        if response.status_code==200:
            print(response.content)
        
        
        
        
    
        
            
      

     
         
      
#async def uvi():
 #   config = uvicorn.Config("app.main:app", port=5000, log_level="info")
  #  server = uvicorn.Server(config)
   # await server.serve()

    
if __name__ == "__main__":
    gui = QtWidgets.QApplication([])
    window = MainWindow()
    #asyncio.run(uvi())
    window.show()
    gui.exec_()