from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

driver = Chrome()
driver.get("http://127.0.0.1:5000/")

#ingresa usuario
driver.find_element_by_name('user').send_keys("prueba0")
#ingresa Contrasena
driver.find_element_by_name('pass').send_keys("prueba0")

#dar click en el boton
driver.find_element_by_id("login").click()

driver.quit()
