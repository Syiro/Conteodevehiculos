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
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
import sqlite3
from datetime import datetime

# Crear la conexión a la base de datos
        # Conectarse a la base de datos
cnx = mysql.connector.connect(user='root', password='Syiro2101.',
                                host='127.0.0.1',
                                database='mydb')

# Crear un cursor para ejecutar consultas
cursor = cnx.cursor()
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
df = pd.DataFrame(resultados, columns=["nombre", "telefono", "mail", "brillo", "contraste", "color", "redneuronal", "modo", "skipfps", "treshold", "fecha", "carrosdetectados", "nombremunicipio", "nombredepartamento"])
df['fecha'] = pd.to_datetime(df['fecha']).dt.floor('min')
df_grouped = df.groupby('fecha')['carrosdetectados'].sum()
plt.plot(df_grouped,color="#808080")
plt.tick_params(axis='x', labelrotation=90)
plt.xlabel('Fecha')
plt.ylabel('Carros detectados')
plt.title('Carros detectados por fecha')
plt.savefig('carros_detectados.png')


# Crear el objeto Canvas para generar el reporte en PDF
documentTitle = 'sample'
title = 'Reporte de congestión'
subTitle = 'The largest thing now!!'
pdf = canvas.Canvas("reporte.pdf", pagesize=letter)
# Agregar el título al reporte
pdf.setFont("Helvetica-Bold", 8)
pdf.setTitle(documentTitle)
pdf.drawCentredString(300, 770, title)
pdf.drawCentredString(300, 760, " Aplicativo para la detección de vehículos en una vía semaforizada")
pdf.drawImage("/home/ruben-laptop/Tesis/code/icons/logoUV_Gris.jpg", 50, 730, width=0.5*inch, height=0.5*inch)
pdf.drawImage("/home/ruben-laptop/Tesis/code/icons/psi.png", 450, 730, width=2*inch, height=0.5*inch)



# drawing a line
pdf.line(30, 720, 590, 720)
textLines = [
    ('Usuario: ', str(resultados[0][0])),
    ('Número de teléfono: ', str(resultados[0][1])),
    ('Correo electrónico: ', str(resultados[0][2])),
    ('Modelo de deteccion: ', str(resultados[0][6])),
    ('Ubicación: ', str(resultados[0][13] + ' ' + str(resultados[0][12])))
]

# creating a multiline text using
# textLines and for loop
text = pdf.beginText(40, 698)
text.setFont("Helvetica", 12)
text.setFillColor(colors.black)

for line in textLines:
    text.setFont("Helvetica-Bold", 12)
    text.textOut(line[0])
    text.setFont("Helvetica", 12)
    text.textLine(line[1])
    
    

pdf.drawText(text)

columnas = [6,7,8,9,10,11] 
ultima_fila = resultados[-1]
resultados_filtrados = [ultima_fila[i] for i in columnas]
nombres_columnas = ["Red neuronal", "Modo", "Skip FPS", "Treshold", "Fecha", "N. Autos"]

fecha_str = ultima_fila[10]
fecha_datetime = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S.%f")

# Formatear la fecha
fecha_formateada = fecha_datetime.strftime("%d/%m/%Y %H:%M:%S")

resultados_filtrados[4] = fecha_formateada

resultados_filtrados = [nombres_columnas, resultados_filtrados]

tabla = Table(resultados_filtrados, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 0.8*inch, 1.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1.5*inch, 1*inch, 1.5*inch, 1.5*inch])
tabla.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#808080')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.black),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 8),
    ('FONTSIZE', (0,1), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,0), 8),
    ('BOTTOMPADDING', (0,1), (-1,-1), 8),
    ('BACKGROUND', (0,1), (-1,-1), colors.white),
    ('GRID', (0,0), (-1,-1), 1, colors.black),
]))

pdf.drawImage("carros_detectados.png", 100, 350, width=6*inch, height=4*inch)


tabla.wrapOn(pdf, 800, 500)
tabla.drawOn(pdf, 40, 280)

# Agregar el pie de página al reporte
pdf.setFont("Helvetica", 10)
fecha_actual = datetime.now().strftime("%d/%m/%Y")

pdf.drawCentredString(415, 30, "Fecha de generación: " + fecha_actual)

# Cerrar el objeto Canvas y guardar el reporte en PDF
pdf.save()
# Cerrar el cursor y la conexión a la base de datos
cursor.close()
cnx.close()