import csv

"""
Este funcion crea el archivo csv para las pruebas automatizadas y para las pruebas de estres y de carga
"""
fields = ["Nombres", "Apellidos", "Fecha de Nacimiento", "Tipo de Documento", "Numero Documento", "Departamento", "Municipio", "Barrio", "Direccion", "Genero", "Telefono", "Correo", "Usuario", "Contrasena", "Estrato"]
filename = "data.csv"

with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for i in range(1000):
        var = "prueba{0}".format(i)
        row = [var, var, "07/06/2021", "CC", i, "Valle del Cauca", "Cali", "Caney", var, "Hombre", i, var+"@gmail.com", var, var, 3]
        csvwriter.writerow(row)
