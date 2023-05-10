import json
import requests
import mysql.connector

from sqlalchemy import desc

import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.pdfgen import canvas
import sqlite3
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
            resultados = cursor.fetchall()

            # Definir el tamaño de la página en formato landscape
            pagina = landscape(letter)

            # Crear el objeto Canvas para generar el reporte en PDF
            pdf = canvas.Canvas("reporte.pdf", pagesize=pagina)

            # Agregar el título al reporte
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawCentredString(415, 750, "Reporte de registros de usuarios")

            # Crear la tabla con los datos de los usuarios
            tabla = Table(resultados, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 0.8*inch, 1.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1.5*inch, 1*inch, 1.5*inch, 1.5*inch])
            tabla.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#8FCACA')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 12),
                ('FONTSIZE', (0,1), (-1,-1), 10),
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ('BOTTOMPADDING', (0,1), (-1,-1), 8),
                ('BACKGROUND', (0,1), (-1,-1), colors.white),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
            ]))

            # Agregar la tabla al reporte y cerrar el objeto Canvas
            # Agregar la tabla al reporte
            tabla.wrapOn(pdf, 800, 500)
            tabla.drawOn(pdf, 40, 500)

            # Agregar un espacio en blanco para separar la tabla del pie de página
            espacio = Spacer(1, 20)
            espacio.wrapOn(pdf, 800, 50)
            espacio.drawOn(pdf, 0, 0)

            # Agregar el pie de página al reporte
            pdf.setFont("Helvetica", 10)
            pdf.drawCentredString(415, 40, "Generado por: ReportLab")
            pdf.drawCentredString(415, 30, "Fecha de generación: 02/05/2023")

            # Cerrar el objeto Canvas y guardar el reporte en PDF
            pdf.save()
           # Cerrar el cursor y la conexión a la base de datos
            cursor.close()
            cnx.close()
             #       Cerrar el cursor y la conexión a la base de datos
