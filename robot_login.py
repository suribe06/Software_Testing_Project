from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
import csv

driver = webdriver.Firefox(executable_path='/home/nicolasibagon/Escritorio/geckodriver')
driver.get("http://127.0.0.1:5000/")

with open('data_login.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    cont = 0
    for row in csv_reader:
        try:
            user = row[0]
            passw = row[1]
            #ingresa usuario
            driver.find_element_by_name('user').send_keys(user)
            #ingresa Contrasena
            driver.find_element_by_name('pass').send_keys(passw)

            #dar click en el boton
            driver.find_element_by_id("login").click()

            #cerras sesion
            element = driver.find_element_by_id('dropdownMenu2')
            ActionChains(driver).click(element).perform()

            #Cerrar sesion
            driver.find_element_by_id("cs").click()
            print("el caso", cont, "pasó")
        except NoSuchElementException:
            print("el caso", cont, "no pasó")
        cont +=1

driver.quit()
