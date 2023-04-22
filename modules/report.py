import json
import requests
import mysql.connector

from sqlalchemy import desc

import pandas as pd
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas


class Reporte:
    
    def hora(self,horainit,horafin):
        self.horainit=horainit
        self.horafin=horafin
        print("Imprimiento hora",horainit,horafin)
        
    def fecha(self,fechainit,fechafin):
        self.fechainit=fechainit
        self.fechafin=fechafin
        print("imprimiendo fechas",fechainit,fechafin)
        
    def insertuser(self,nombre,telefono,email):
        
        url = 'http://127.0.0.1:8000/usuarios/'
        pyload = {'nombre':nombre,'telefono':telefono,'mail':email}
        data=json.dumps(pyload) 
        response = requests.post(url, data)
        if response.status_code == 200:
            print(response.content)

    
    def insertcity(self,municipio):
        url = 'http://127.0.0.1:8000/municipios/'
        pyload = {'nombremunicipio':municipio}
        data=json.dumps(pyload) 
        response = requests.post(url, data)
        if response.status_code == 200:
            print(response.content)

            
    def insertdepa(self,departamentos):
        url = 'http://127.0.0.1:8000/departamentos/'
        pyload = {'nombredepartamento':departamentos}
        data=json.dumps(pyload) 
        response = requests.post(url, data)
        if response.status_code == 200:
            print(response.content)
    
            
    def reporte(self):
        
# Crear la conexión a la base de datos
                    # Conectarse a la base de datos
            cnx = mysql.connector.connect(user='root', password='Syiro2101.',
                                            host='127.0.0.1',
                                            database='mydb')

            # Crear un cursor para ejecutar consultas
            cursor = cnx.cursor()

            # Ejecutar la consulta utilizando la sentencia SQL de JOIN

            query ="SELECT usuarios.nombre,\
                            usuarios.telefono, usuarios.mail, configuracion.brillo, configuracion.contraste,\
                            configuracion.color, configuracion.redneuronal, configuracion.modo, configuracion.skipfps,\
                            configuracion.treshold, datossemaforo.fecha, datossemaforo.carrosdetectados,\
                            municipios.nombremunicipio, departamentos.nombredepartamento\
                    FROM usuarios\
                    LEFT JOIN configuracion ON usuarios.idusuarios = configuracion.idconfiguracion\
                    right JOIN datossemaforo ON usuarios.idusuarios = datossemaforo.idcarros\
                    LEFT JOIN municipios ON usuarios.idusuarios = municipios.idmunicipios\
                    LEFT JOIN departamentos ON municipios.idmunicipios = departamentos.iddepartamentos;"                  
            cursor.execute(query)

            # Obtener los resultados de la consulta utilizando el método fetchall()
            results = cursor.fetchall()

            # Crear un dataframe de Pandas con los resultados
            columns = ['Nombre', 'Teléfono', 'Correo', 'Brillo', 'Contraste', 'Color', 'Red neuronal', 'Modo', 'Skip FPS', 'Treshold', 'Fecha', 'Autos contados', 'Municipio', 'Departamento']
            df = pd.DataFrame(results, columns=columns)

            # Crear una tabla en el PDF utilizando Pandas
            pdf = canvas.Canvas("reporte.pdf")
            pdf.drawString(100, 750, "Reporte de registros de usuarios")
            y = 700
            for row in df.iterrows():
                y -= 20
                pdf.drawString(100, y, f"{row[1]['Nombre']}")
                pdf.drawString(200, y, f"{row[1]['Teléfono']}")
                pdf.drawString(300, y, f"{row[1]['Correo']}")
                pdf.drawString(400, y, f"{row[1]['Autos contados']}")
                pdf.drawString(500, y, f"{row[1]['Fecha']}")
            pdf.drawString(100, y-40, "Tabla de usuarios")
            pdf.save()

            # Crear un gráfico de barras utilizando Matplotlib
            fig, ax = plt.subplots(figsize=(8,6))
            df['Municipio'].value_counts().plot(kind='bar', ax=ax)
            ax.set_xlabel('Municipio')
            ax.set_ylabel('Cantidad de usuarios')
            ax.set_title('Distribución de usuarios por municipio')
            plt.savefig('barras.png')
            plt.close()

            # Cerrar el cursor y la conexión a la base de datos
            cursor.close()
            cnx.close()
                    # Cerrar el cursor y la conexión a la base de datos
