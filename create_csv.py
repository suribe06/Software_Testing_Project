import csv

"""
Este archivo posee las funciones para crear los archivos csv para las pruebas automatizadas y para las pruebas de estres y de carga
"""

def create_data_register():
    filename = "data_register.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for i in range(20):
            var = "prueba{0}".format(i)
            row = [var, var, i, var, i, var+"@gmail.com", var, var]
            csvwriter.writerow(row)

def create_data_login():
    filename = "data_login.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for i in range(20):
            var = "prueba{0}".format(i)
            row = [var, var]
            csvwriter.writerow(row)

create_data_register()
create_data_login()
