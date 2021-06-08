from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

driver = Chrome()
driver.get("http://127.0.0.1:5000/")

#Seleccionar boton para registrarse
driver.find_element_by_id("registro").click()

#Seleccion civil para registrar
select = Select(driver.find_element_by_id('tipoRegistro'))
select.select_by_visible_text('Civil')
driver.find_element_by_id("continuar").click()

#Llenar campos registro
driver.find_element_by_name('nombres').send_keys("prueba0")
driver.find_element_by_name('apellidos').send_keys("prueba0")
#Fecha de Nacimiento
date_input = driver.find_element_by_name('fecha')
date_input.click()
date_input.clear()
date_input.send_keys("05061999")
#Tipo de Documento
select = Select(driver.find_element_by_id('tipoDocumento'))
select.select_by_visible_text('Cedula de Ciudadania')
#Numero de Documento
driver.find_element_by_id('documento').send_keys("0")
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
driver.find_element_by_name('direccion').send_keys("prueba0")
#Genero
select = Select(driver.find_element_by_id('genero'))
select.select_by_visible_text('Hombre')
#Telefono
driver.find_element_by_id('telefono').send_keys("0")
#Correo
driver.find_element_by_id('correo').send_keys("prueba0@gmail.com")
#Usuario
driver.find_element_by_name('username').send_keys("prueba0")
#Contrasena
driver.find_element_by_name('password').send_keys("prueba0")
#Estrato
select = Select(driver.find_element_by_id('estrato'))
select.select_by_visible_text('4')

#Click en registrar
driver.find_element_by_name("Registrarse").click()

driver.quit()
