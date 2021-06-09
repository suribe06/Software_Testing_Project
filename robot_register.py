from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import csv

#driver = webdriver.Firefox(executable_path='/home/nicolasibagon/Escritorio/geckodriver')
driver = Chrome()
driver.get("http://127.0.0.1:5000/")


with open('data_register.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    cont = 1
    for row in csv_reader:
        try:
            name = row[0]
            l_name = row[1]
            n_documento = row[2]
            address = row[3]
            phone = row[4]
            email = row[5]
            user = row[6]
            passw = row[7]
            #Seleccionar boton para registrarse
            driver.find_element_by_id("registro").click()
            #Seleccion civil para registrar
            select = Select(driver.find_element_by_id('tipoRegistro'))
            select.select_by_visible_text('Civil')
            driver.find_element_by_id("continuar").click()
            #Llenar campos registro
            driver.find_element_by_name('nombres').send_keys(name)
            driver.find_element_by_name('apellidos').send_keys(l_name)
            #Fecha de Nacimiento
            date_input = driver.find_element_by_name('fecha')
            date_input.click()
            date_input.clear()
            date_input.send_keys("05061999")
            #date_input.send_keys("1999-05-06")

            #Tipo de Documento
            select = Select(driver.find_element_by_id('tipoDocumento'))
            select.select_by_visible_text('Cedula de Ciudadania')
            #Numero de Documento
            driver.find_element_by_id('documento').send_keys(n_documento)
            #Departamento
            select = Select(driver.find_element_by_id('departamento'))
            select.select_by_visible_text('Valle del Cauca')
            #Municipio
            select = Select(driver.find_element_by_id('municipio'))
            select.select_by_visible_text('Cali')
            #Barrio
            select = Select(driver.find_element_by_id('barrio'))
            select.select_by_visible_text('Caney')
            #Direccion
            driver.find_element_by_name('direccion').send_keys(address)
            #Genero
            select = Select(driver.find_element_by_id('genero'))
            select.select_by_visible_text('Hombre')
            #Telefono
            driver.find_element_by_id('telefono').send_keys(phone)
            #Correo
            driver.find_element_by_id('correo').send_keys(email)
            #Usuario
            driver.find_element_by_name('username').send_keys(user)
            #Contrasena
            driver.find_element_by_name('password').send_keys(passw)
            #Estrato
            select = Select(driver.find_element_by_id('estrato'))
            select.select_by_visible_text('4')

            #Click en registrar

            driver.find_element_by_name("Registrarse").click()
            print("el caso", cont, "pasó")
        except NoSuchElementException:
            print("el caso", cont, "no pasó")
        cont+=1


driver.quit()
