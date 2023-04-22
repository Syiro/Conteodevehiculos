import json
import requests
import mysql.connector
from reportlab.pdfgen import canvas
# Crear la conexión a la base de datos
cnx = mysql.connector.connect(user='root', password='Syiro2101.',
                            host='127.0.0.1',
                            database='mydb')

# Crear un cursor para ejecutar consultas
cursor = cnx.cursor()

# Ejecutar la consulta utilizando la sentencia SQL de JOIN
query ="SELECT usuarios.nombre, usuarios.mail, usuarios.telefono,\
                    configuracion.brillo, configuracion.color, configuracion.contraste,\
                    configuracion.modo, configuracion.redneuronal, configuracion.skipfps,\
                    configuracion.treshold, datossemaforo.fecha, datossemaforo.carrosdetectados\
                FROM usuarios\
                LEFT JOIN configuracion ON usuarios.idusuarios = configuracion.idusuarios\
                LEFT JOIN datossemaforo ON usuarios.idusuarios = datossemaforo.idusuarios;"      
                     
cursor.execute(query)
cursor.close()
cnx.close()
# print(query)
# #Obtener los resultados de la consulta utilizando el método fetchall()
# results = cursor.fetchall()

# # Procesar los resultados y generar el reporte en PDF utilizando la biblioteca reportlab
# pdf = canvas.Canvas("reporte.pdf")
# pdf.drawString(100, 750, "Reporte de registros de usuarios")

# y = 700
# for row in results:
#     nombre = row[0]
#     telefono = row[1]
#     mail = row[2]
#     carrosdetectados = row[3]
#     fecha = row[4]
#     brillo = row[5]
#     contraste = row[6]
#     color = row[7]
#     modo = row[8]
#     redneuronal = row[9]
#     skipfps = row[10]
#     treshold = row[11]

#     pdf.drawString(100, y, f"Nombre: {nombre}")
#     pdf.drawString(100, y-20, f"Teléfono: {telefono}")
#     pdf.drawString(100, y-40, f"Correo: {mail}")
#     pdf.drawString(100, y-60, f"Autos contados: {carrosdetectados}")
#     pdf.drawString(100, y-80, f"Fecha: {fecha}")
#     pdf.drawString(100, y-100, f"Brillo: {brillo}")
#     pdf.drawString(100, y-120, f"Contraste: {contraste}")
#     pdf.drawString(100, y-140, f"Color: {color}")
#     pdf.drawString(100, y-160, f"Modo: {modo}")
#     pdf.drawString(100, y-180, f"Red neuronal: {redneuronal}")
#     pdf.drawString(100, y-200, f"Skip FPS: {skipfps}")
#     pdf.drawString(100, y-220, f"Treshold: {treshold}")
#     y -= 240

# pdf.save()

# # Cerrar el cursor y la conexión a la base de datos
