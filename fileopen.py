from config import *

class FileOpen:

    def fileopen(self,type):
        global fname
        if type =="Video":
            color=1
            cont=1
            brillo=1
            fname,b = QFileDialog.getOpenFileName(self,"Open File",""," Videos (*.mp4 *.wav)")
            self.start_video(a=2) 

        elif type =="Imagenes":
            fname,b = QFileDialog.getOpenFileName(self,'Open File',''," Imagenes (*.jpg *.jpeg *.png)") 
            self.label_18.setPixmap(QPixmap(fname))

        elif type == "red":
            pathname,b = QFileDialog.getOpenFileName(self,'Open File',''," Archivo comprimido (*.zip *.rar)") 
            Ejecucion.Cargaparametros(self,pathmodel=pathname)
            global red
            red = pathname
            self.label_28.setText(pathname)

        elif type =="Tiempo real":
            print("proximamente")
            fname=""
        
        
    def filesave(self,data):
        sname,b = QFileDialog.getSaveFileName(self,'Save file','',"Json (*.json)")
        file = open(sname,'w')
        file.write(data)
        file.close()
    