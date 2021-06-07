from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

driver = Chrome()
driver.get("http://127.0.0.1:5000/")

driver.find_element_by_id("registro").click()

select = Select(driver.find_element_by_id('tipoRegistro'))
select.select_by_visible_text('Civil')
select.select_by_value('C')

driver.find_element_by_id("continuar").click()
